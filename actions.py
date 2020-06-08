from typing import Any, Text, Dict, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.events import AllSlotsReset

from datetime import datetime
import test
import time
from env.Crawl_paper import beautiful_4

class ActionCoreValues(Action):

    def name(self) -> Text:
        return "action_ask_paper"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        topic = tracker.get_slot("topic")
        conference = tracker.get_slot("conference")
        year = tracker.get_slot("year")
        if year == "năm nay":
            x = datetime.now()
            year = x.strftime("%Y")
        elif year == "năm ngoái":
            x = datetime.now()
            year = x.strftime("%Y")
            year = int(year)
            year = str(year - 1)
        elif year == "năm kia":
            x = datetime.now()
            year = x.strftime("%Y")
            year = int(year)
            year = str(year - 2)
        
        dispatcher.utter_message("Em đang tìm kiếm câu trả lời phù hợp nhất. Anh (chị) đợi em một lát ạ ^-^")

        url = beautiful_4.CreateURl(conference, topic, year)
        ans = beautiful_4.CrawlPaper(10, url)
        time.sleep(5)
        
        for s in ans:
            dispatcher.utter_message(s)
    
        AllSlotsReset()
        

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
        if since is not None:
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

class ActionCoreValues(Action):

    def name(self) -> Text:
        return "action_ask_competition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trả về các cuộc thi đang hoặc sắp diễn ra trên kaggle
        url = "https://www.kaggle.com/competitions"
        dispatcher.utter_message("Các cuộc thi đang diễn ra trên kaggle là: {}".format(url))

        # Code xử lý trả về kết quả

class ActionCoreValues(Action):

    def name(self) -> Text:
        return "action_ask_conference"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trả về danh sách các hội thảo theo yêu cầu. Nếu không nói cụ thể sẽ trả về hết các hội thỏa trong năm
        time = tracker.get_slot("time")
        if time is None:
            time = "năm nay"
        url = "http://www.guide2research.com/topconf/"
        dispatcher.utter_message("Các hội thảo năm nay là: {}".format(url))

        # Code xử lý trả về kết quả


class ActionCoreValues(Action):

    def name(self) -> Text:
        return "action_suggest_medium"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trả về các bài viết hay trên medium
        url = "https://medium.com/search?q=machine%20learning"
        dispatcher.utter_message("Những bài viết hay trên medium là: {}".format(url))

        # Code xử lý trả về kết quả