from typing import Any, Text, Dict, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.events import AllSlotsReset

from datetime import datetime
import test
import time
from Crawl_paper import beautiful_4
from functools import lru_cache
import lxml
from lxml import html
import xml.etree.cElementTree as etree


@lru_cache(maxsize=64)
def get_papers(conference, topic, year):
    url = beautiful_4.CreateURl(conference, topic, year, number_of_paper=5)
    ans = beautiful_4.CrawlPaper(url)
    return ans

class ActionAskPaper(Action):

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

        ans = ""
        if topic is None and conference is None:
            ans = "Dạ, anh chị vui lòng tìm kiếm paper giúp em theo form sau với ạ: \n \"paper về + tên bài toán anh chị muốn hỏi\""
        else:
            ans += "Dạ, em tìm được 1 số câu trả lời này, anh (chị) xem có phù hợp không ạ. \n"
            if year is None:
                year = 2020
            ans += "[info]" +get_papers(conference, topic, year) + "[/info]"
        
        dispatcher.utter_message(ans)
    
        return [AllSlotsReset()]
        

class ActionAskTrending1(Action):

    def name(self) -> Text:
        return "action_ask_trending1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trả về trending, lấy 5 trending trên trang github và 5 trending trên trang paperwithcode. Mặc định trend github lấy language = python, since=daily
        url_github = "https://github.com/trending/python?since=daily"
        url_paperwithcode = "https://paperswithcode.com/search?q_meta=&q=trending"
        ans = "Dạ, hiện tại trên trang github và paperwithcode đang có những trend này. Anh (chị) tham khảo xem có hứng thú không ạ:" + "\n"

        # Code xử lý trả về kết quả
        ans_git = beautiful_4.Trending_github(url_github, 5)
        ans_paper = beautiful_4.Trending_paperwithcode(url_paperwithcode, 5)
        ans += "[info]"
        ans += "Trending GitHub:" + "\n" + ans_git + "\n"
        ans += "Trending Paperwithcode:" + "\n" + ans_paper + "\n"
        ans += "[/info]"
        
        dispatcher.utter_message(ans)

        return [AllSlotsReset()]

class ActionAskTrending2(Action):

    def name(self) -> Text:
        return "action_ask_trending2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trả về 10 trending trên github
        daily = ["hiện nay", "hiện giờ", "hôm nay", "dạo này", "gần đây"]
        since = tracker.get_slot("time")
        if since is None:
            since = "hôm nay"
        ans = "Dạ trending github " + since + " là: \n"
        since = since.lower()
        if since in daily:
            since = "daily"
        elif since == "tuần này":
            since = "weekly"
        else:
            since = "monthly"
        url = "https://github.com/trending/python?since=" + since
        trend = beautiful_4.Trending_github(url, 10)
        ans += "[info]"
        ans += trend + "[/info]"
        dispatcher.utter_message(ans)

        return [AllSlotsReset()]

class ActionAskTrending3(Action):

    def name(self) -> Text:
        return "action_ask_trending3"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trả về 10 trending trên trang paperwithcode. URL trending trên paperwithcode là mặc định
        url = "https://paperswithcode.com/search?q_meta=&q=trending"

        ans = "Dạ, trending paperwithcode là: \n"
        trend = beautiful_4.Trending_paperwithcode(url, 10)
        ans += "[info]" + trend + "[/info]"
        dispatcher.utter_message(ans)
        return [AllSlotsReset()]

       
class ActionAskCompetiton(Action):

    def name(self) -> Text:
        return "action_ask_competition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trả về các cuộc thi đang hoặc sắp diễn ra trên kaggle

        competitions = beautiful_4.crawl_competitions()
        ans = "Dạ! , competitions đang có là: \n "
        ans += "[info]" + competitions + "[/info]"
        dispatcher.utter_message(ans)
        
        return [AllSlotsReset()]

class ActionAskConference(Action):

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
        ans = "Dạ, danh sách các hội thảo " + time + " là: \n"
        conferences = beautiful_4.crawl_conference(url, 20)
        ans += "[info]" + conferences + "[/info]"
        dispatcher.utter_message(ans)

        return [AllSlotsReset()]


class ActionSuggestMedium(Action):

    def name(self) -> Text:
        return "action_suggest_medium"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trả về các bài viết hay trên medium
        url = "https://medium.com/search?q=machine%20learning"

        ans = "Dạ, trên Medium đang có một vài bài viết hay và được rất nhiều người quan tâm, anh chị có thể tham khảo ạ: \n"

        ans += "[info]" + beautiful_4.crawl_medium() + "[/info]"

        dispatcher.utter_message(ans)

        # Code xử lý trả về kết quả