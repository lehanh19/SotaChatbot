import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from rasa.core.channels.channel import (
    InputChannel,
    OutputChannel,
    UserMessage,
    CollectingOutputChannel,
    QueueOutputChannel
)
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
import json
import asyncio
import re
import requests
import base64, hmac, hashlib
from asyncio import Queue, CancelledError
from typing import Text, Dict, Any, Optional, Callable, Awaitable
import threading
import time
from pprint import pprint
from datetime import datetime
import pytz
tz = pytz.timezone('Asia/Ho_Chi_Minh')

# people's name, will be initialized at first message in
db = None
api_ = None
last = None

def update_request():
    '''
    add new contacts.
    '''
    # logger.info("Fetching new requests...")
    ret = requests.get("https://api.chatwork.com/v2/incoming_requests",
                       headers={"X-ChatWorkToken": api_})
    # for some reason, it doesn't return an empty dict if no requests available, rather an empty byte.
    if len(ret.content) > 0:
        for contact in ret.json():
            requests.put(f"https://api.chatwork.com/v2/incoming_requests/{contact['request_id']}",
                                   headers={"X-ChatWorkToken": api_})
            db[contact["account_id"]] = contact["name"]

lock = threading.Lock()
class UpdateFriends(threading.Thread):
    def run(self):
        while True:
            if db is not None:
                with lock:
                    update_request()
            time.sleep(5)

t = UpdateFriends()
t.daemon = True
t.start()

class ChatworkOutput(OutputChannel):
    @classmethod
    def name(cls):
        return "chatwork"

    def __init__(self,
            token_api: Text,
            sender_id: int,
            room_id: int,
            message_id: int
        ) -> None:
        self.room_id = room_id
        self.sender_id = sender_id
        self.message_id = message_id
        self.header = {"X-ChatWorkToken": token_api}

    async def send_text_message(
        self, recipient_id: Optional[Text], text: Text, **kwargs: Any
    ) -> None:
        uri = "https://api.chatwork.com/v2/rooms/" + str(self.room_id) + "/messages"
        text = f'[rp aid={self.sender_id} to={self.room_id}-{self.message_id}]' + \
               f'{db[self.sender_id] if self.sender_id in db else "Người lạ"}\n' + text
        data = {"body": text}
        requests.post(uri, headers=self.header, data=data)


class ChatworkInput(InputChannel):
    @classmethod
    def name(cls) -> Text:
        return "chatwork"

    @classmethod
    def from_credentials(cls, credentials):
        if not credentials:
            cls.raise_missing_credentials_exception()
        return cls(credentials.get("api_token"), credentials.get("secret_token"))

    def __init__(self, api_token: Text, secret_token: Text) -> None:
        self.api_token = api_token
        self.secret_token = secret_token

        # fetch people's name
        global db, api_
        logger.info("Initializing user database...")
        db = dict()
        api_ = api_token
        for contact in requests.get("https://api.chatwork.com/v2/contacts",
                                   headers={"X-ChatWorkToken": api_}).json():
            db[contact["account_id"]] = contact["name"]
        with lock: update_request()


    @staticmethod
    def _sanitize_user_message(text):
        """
        Remove all tags.
        """
        text = text.strip()

        # these tags don't warrant a newline removal
        for regex, replacement in [
            (r"\[/?qt(meta aid=\d+( time=\d+)?)?\]", ""),
            (r"\[/?Quote( aid=\d+ time=\d+)?\]", ""),
            (r'\[/?info\]', ''),
            (r'\[/?code\]', ''),
            (r'\[hr\]', ''),
            (r'\[picon(name)?:\d+\]', ''),
        ]:
            text = re.sub(regex, replacement, text).strip()

        # HACK: iteratively remove first-line mentions.
        newline_regex = [
            # to messages
            (r"\[[Tt][Oo]:\d+\]", ""),
            # reply messages
            (r"\[[Rr][Pp] aid=[^]]+\]", ""),
            (r"\[Reply aid=[^]]+\]", ""),
        ]
        while True:
            found = {}
            for regex, replacement in newline_regex:
                re_res = re.search(regex, text)
                if re_res is not None:
                    found[re_res.start(0)] = (regex, replacement)
            if len(found) == 0:
                return text
            if min(found.keys()) > 0:
                for regex, replacement in found.values():
                    text = re.sub(regex, replacement, text).strip()
                return text
            regex, replacement = found[0]
            text = re.sub(regex + r'[^\n]*\n', replacement, text, count=1).strip()

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        custom_webhook = Blueprint("chatwork_webhook", "chatwork"
        )

        # pylint: disable=unused-variable
        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"signature_tag": "o' kawaii koto."})

        def validate_request(request):
            # Check the X-Hub-Signature header to make sure this is a valid request.
            chatwork_signature = request.headers.get('X-ChatWorkWebhookSignature', '')
            signature = hmac.new(base64.b64decode(bytes(self.secret_token, encoding='utf-8')),
                                 request.body,
                                 hashlib.sha256)
            expected_signature = base64.b64encode(signature.digest())

            return hmac.compare_digest(bytes(chatwork_signature, encoding='utf-8'),
                                       expected_signature)

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request) -> HTTPResponse:

            if not validate_request(request):
                return response.json("you've been a very bad boy!", status=400)

            # print(request.body)
            # pprint(request.headers)
            content = request.json["webhook_event"]
            # pprint(content)

            # ignore edit events
            if content["update_time"] > 0:
                return response.json("✅ seen")

            sender_id = content["from_account_id"]
            # update contacts
            if sender_id not in db:
                with lock: update_request()

            room_id = content["room_id"]
            message_id = content["message_id"]
            # again, remember that this is a hack.
            text = self._sanitize_user_message(content["body"])
            metadata = {
                "sender_id": str(sender_id),
                "room_id": str(room_id),
                # already string, change this when Chatwork goes dumb dumb
                "message_id": message_id
            }

            username = db[sender_id] if sender_id in db else f"Người lạ ({sender_id})"
            print(f'{datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")} {username:>36}: {text}')

            out_channel = self.get_output_channel(sender_id, room_id, message_id)
            try:
                await on_new_message(
                    UserMessage(
                        text,
                        out_channel,
                        sender_id,
                        input_channel=room_id,
                        metadata=metadata,
                    )
                )
            except CancelledError:
                logger.error(
                    "Message handling timed out for "
                    "user message '{}'.".format(text)
                )
            except Exception:
                logger.exception(
                    "An exception occured while handling "
                    "user message '{}'.".format(text)
                )
            return response.json("alles gut 👌")

        return custom_webhook

    def get_output_channel(self, sender_id, room_id, message_id) -> OutputChannel:
        return ChatworkOutput(self.api_token, sender_id, room_id, message_id)
