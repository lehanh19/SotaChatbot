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

        dispatcher.utter_message("Dạ, em đang tìm kiếm câu trả lời phù hợp nhất với yêu cầu của anh chị. Anh (chị) đợi em một lát ạ ^-^")

        if year is None:
            year = 2020
        ans = get_papers(conference, topic, year)
        # print(ans)
        # time.sleep(5)
        
        for s in ans:
            dispatcher.utter_message(s)
    
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
        dispatcher.utter_message("Dạ, hiện tại trên trang github và paperwithcode đang có những trend này. Anh (chị) tham khảo xem có hứng thú không ạ:")

        # Code xử lý trả về kết quả
        ans_git = beautiful_4.Trending_github(url_github, 5)
        ans_paper = beautiful_4.Trending_paperwithcode(url_paperwithcode, 5)
        ans1 = "Trending GitHub:" + "\n" + ans_git
        ans2 = "Trending Paperwithcode:" + "\n" + ans_paper
        dispatcher.utter_message(ans1)
        dispatcher.utter_message(ans2)

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
        ans += trend
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
        ans += trend
        dispatcher.utter_message(ans)
        AllSlotsReset()

       
class ActionAskCompetiton(Action):

    def name(self) -> Text:
        return "action_ask_competition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trả về các cuộc thi đang hoặc sắp diễn ra trên kaggle

        competitions = beautiful_4.crawl_competitions()
        ans = "Dạ! , competitions đang có là: \n "
        dispatcher.utter_message(ans)
        for info in competitions.split("\n"):
            dispatcher.utter_message(info)
        # ans +=competitions

        # dispatcher.utter_message(ans)
        AllSlotsReset()

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
        ans += conferences
        dispatcher.utter_message(ans)

        AllSlotsReset()


class ActionSuggestMedium(Action):

    def name(self) -> Text:
        return "action_suggest_medium"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Trả về các bài viết hay trên medium
        url = "https://medium.com/search?q=machine%20learning"
        dispatcher.utter_message("Những bài viết hay trên medium là: {}".format(url))

        # Code xử lý trả về kết quả