from typing import Any, Text, Dict, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.events import AllSlotsReset

from datetime import datetime

class ActionCoreValues(Action):

    def name(self) -> Text:
        return "action_ask_paper3"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trả về các paper cần tìm theo hội nghị và năm
        keyword = tracker.get_slot("keyword")
        conference = tracker.get_slot("conference")
        year = tracker.get_slot("year")
        if year == "năm nay":
            x = datetime.now()
            year = x.strftime("%Y")
        dispatcher.utter_message("keyword, conference, year: {}, {}, {}".format(keyword, conference, year))

        # Code xử lý trả về kết quả
        

class ActionCoreValues(Action):

    def name(self) -> Text:
        return "action_ask_paper2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trả về các paper theo hội nghị và năm
        conference = tracker.get_slot("conference")
        year = tracker.get_slot("year")
        if year == "năm nay":
            x = datetime.now()
            year = x.strftime("%Y")
        dispatcher.utter_message("conference, year: {}, {}".format(conference, year)) # Trả về kết quả cho user

        # Code xử lý trả về kết quả


class ActionCoreValues(Action):

    def name(self) -> Text:
        return "action_ask_paper1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trả về các paper theo yêu cầu
        keyword = tracker.get_slot("keyword")
        dispatcher.utter_message("keyword: {}".format(keyword))

        # Code xử lý trả về kết quả

class ActionCoreValues(Action):

    def name(self) -> Text:
        return "action_ask_trending1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trả về trending, lấy 5 trending trên trang github và 5 trending trên trang paperwithcode. Mặc định trend github lấy language = python, since=daily
        url_github = "https://github.com/trending/python?since=daily"
        url_paperwithcode = "https://paperswithcode.com/"
        dispatcher.utter_message("Trending hiện nay là:")

        # Code xử lý trả về kết quả

class ActionCoreValues(Action):

    def name(self) -> Text:
        return "action_ask_trending2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trả về 10 trending trên github
        daily = ["hiện nay", "hiện giờ", "hôm nay", "dạo này", "gần đây"]
        since = tracker.get_slot("time")
        since = since.lower()
        if since in daily:
            since = "daily"
        elif since == "tuần này":
            since = "weekly"
        else:
            since = "monthly"
        url = "https://github.com/trending/python?since=" + since
        dispatcher.utter_message("url trả về là: {}".format(url))

        # Code xử lý trả về kết quả

class ActionCoreValues(Action):

    def name(self) -> Text:
        return "action_ask_trending3"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trả về 10 trending trên trang paperwithcode. URL trending trên paperwithcode là mặc định
        url = "https://paperswithcode.com/"
        dispatcher.utter_message("Trending trên trang paperwithcode là: {}".format(url))

        # Code xử lý trả về kết quả