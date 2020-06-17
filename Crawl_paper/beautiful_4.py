from bs4 import BeautifulSoup
import requests
import argparse
import time
import os
import sys
import lxml
import kaggle
from lxml import html
from shell import shell
import xml.etree.cElementTree as etree


def CreateURl(Conference=None, Keywork=None, Year=2020, number_of_paper=5):
    urlparser_first = 'http://export.arxiv.org/api/query?search_query='
    urlparser_last = '&start=0&max_results=' + str(number_of_paper)

    if Keywork is None:
        Keywork = ""

    ans = Keywork.strip()
    Year = str(Year)

    if Conference is not None:
        Conference = Conference.strip()
        ans += " " + Conference
    ans += " " + Year

    url_ = urlparser_first + ans.replace(' ', '+') + urlparser_last

    return url_


def CrawlPaper(url=None):
    ans = ""
    try:
        r = requests.get(url)
    except OSError:
        ans = "cannot open your requests URL, maybe something wrong. Please check again !"
        return ans
    envv = html.fromstring(r.content)
    link_list = envv.xpath('//link[@title="pdf"]')
    summary = envv.xpath('//summary')
    link_summary = envv.xpath('//entry')

    if min(len(link_list), len(summary)) is 0:
        ans = "Sorry!. Your query has no results."
        return ans

    for index in range(len(summary)):
        s = ""
        see = summary[index].text.replace("\n", " ").strip()
        sublink = link_list[index].attrib['href']
        sublink_summary = link_summary[index].find('id').text

        s += str(index + 1) + "." + see + "\n"
        s += "Link paper: " + sublink + "\n"
        s += "Link summary paper: " + sublink_summary + "\n"
        s += "========================================== \n "
        ans += s
    return ans

def Trending_github(url=None, number_of_trend=None):
    """ crawl data in github.com/trending """
    "" " url = https://github.com/trending/python?since=monthly """

    s = ""
    try:
        r = requests.get(url)
    except OSError:
        s = " something wrong, pls check url again ! "
        return s
    if number_of_trend is not None:
        number_of_trend = min(number_of_trend, 25)
    origin_link = 'https://github.com'
    soup = BeautifulSoup(r.text, 'lxml')
    all_trend = soup.find_all("article", {"class": "Box-row"})
    for index, trend in enumerate(all_trend):
        if index == number_of_trend:
            break
        suffix_link = trend.find('h1', {"class": "h3 lh-condensed"}).a.get("href").strip()
        result = origin_link + suffix_link
        decription = str(index + 1) + ". " + trend.find("p", {"class": "col-9 text-gray my-1 pr-4"}).text.strip()
        s += "\n" + decription + "\n" + result + "\n" + " ======================== "
# this function return list of row, every single row must print in one line.
    return s


def Trending_paperwithcode(url=None, number_of_trending=None):
    """ crawl in link 'https://paperswithcode.com/search?q_meta=&q=trending' """
    try:
        r = requests.get(url)
    except OSError:
        return " sorry !. Something wrong with URL just check it again !"

    result = ""
    origin_PaperWithCode = 'https://paperswithcode.com'

    soup = BeautifulSoup(r.text, 'lxml')
    list_trend = soup.find_all('div', {"class": "row infinite-item item"})
    if number_of_trending is not None:
        number_of_trending = min(number_of_trending, len(list_trend))
    
    for index, trend in enumerate(list_trend):
        if index == number_of_trending:
            break
        link = trend.find('h1').a.get('href').strip()
        full_link = origin_PaperWithCode + link
        decription = str(index + 1) + ". " + trend.find("h1").text.strip()
        result += decription + "\n" + full_link + "\n"
    return result


def crawl_conference(url=None, number_of_conference=None):
    """ crawl in http://www.guide2research.com/topconf/ """
    try:
        r = requests.get(url)
    except OSError:
        return "Sorry !, something wrong with your url ! "

    origin_conference = 'http://www.guide2research.com'

    conference_list = BeautifulSoup(r.text,'lxml')
    list_ans = conference_list.find_all('div', {"class": "grey myshad"})

    if number_of_conference is not None:
        number_of_conference = min(number_of_conference, len(list_ans))
    result = ""
    for index, value in enumerate(list_ans):
        if len(value.table.tr.find_all('a')) is 0:
            continue
        if index >= number_of_conference:
            break
        suffix = value.table.tr.find_all('a')[0]['href'].strip()
        link_summary = origin_conference + suffix
        text = str(index + 1) + ". " + value.table.tr.find_all('a')[0].text.strip()
        link_conference = value.table.find_all('a', {"target": "_blank"})[0]['href'].strip()

        result += text + "\n" + "link summary conference: " + link_summary + "\n" + "link conference:         " + link_conference + "\n"
    return result

def crawl_competitions():

    """ we using Kaggle API for crawl competitions """

    READ_SHELL_COMMAND = shell('kaggle competitions list')
    information = []
    for file in READ_SHELL_COMMAND.output():
        information.append(file)

    result = ""
    link_perfix = 'https://www.kaggle.com/c/'
    for index, value in enumerate(information):
        if index == 1 :
            continue
        value = value.replace("userHasEntered","").replace("True","").replace("False","")
        result += value + "\n"
        if index >1:
            link = "Link: " + link_perfix + value.split(" ")[0] + "\n"
            result +=link


    return result

def crawl_medium():
    """ we crawl articles in medium.com """
    url = "https://medium.com/topic/artificial-intelligence"
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    root = soup.find('div',{'class':'a b c'}).find('div',{'class':'n p'}).find('div',{'class':'z ab ac ae af ag ah ai'})

#         crawl main artiles
    articles_main = root.find_next('div').find_all_next('section')
    ans = ''
    for index, item in enumerate(articles_main):
        if index % 2 == 0:
            continue
        content = item.find('a').text
        link = item.find('a').attrs['href']
        if link.split('//')[0] != 'https:':
            link = 'https://medium.com' + link
        ans += content  + '\n'
        ans += link + '\n'
        ans += '============================ \n'
    # crawl popular articles
    pupolar_articles = root.find_all_next('div',{'class':'r bv'})
    ans += '\n' + 'POPULAR IN ARTIFICIAL INTELLIGENCE' + '\n'
    for index, item in enumerate(pupolar_articles):
        if index % 2 == 1:
            continue
        link = item.find('a').attrs['href']
        title = item.find('h4').text
        ans += title + '\n'
        ans += link + '\n'
    return ans


def _main_(args):
    if __name__ == '__main__':
        keyword_search = ' '.join(args.keyword)
        conference_search = ' '.join(args.conference)
        year_search = args.year
        num = args.number
# crawl paper
        print(" crawling paper ...............")
        url_origin = CreateURl(Conference=conference_search, Keywork=keyword_search, Year=year_search,number_of_paper=num)
        print(url_origin)
        ans = CrawlPaper(url=url_origin)
        for item in ans:
            print(item)
# crawl trending in github.com/trending
        print("crawling trend/github................")
        # time.sleep(5)
        ans = Trending_github('https://github.com/trending/python?since=monthly',50).split("\n")
        for item in ans:
            print(item)
# crawl trending in paper with code
        print("crawling trend paper with code............................")
        # time.sleep(5)
        ans = Trending_paperwithcode('https://paperswithcode.com/search?q_meta=&q=trending', 100).split("\n")
        for item in ans:
            print(item)
# crawl conference
        print("crawling conference .............................")
        # time.sleep(5)
        ans = crawl_conference('http://www.guide2research.com/topconf/',number_of_conference = 6).split("\n")
        for item in ans:
            print (item)
# crawl competitions
        print("crawling competitions in kaggle")
        ans = crawl_competitions()
        print(ans)

        print("end .................................................")


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='test crawl paper')

    argparser.add_argument(
        '-k',
        '--keyword',
        nargs='+',
        default="",
        help='pass keyword')

    argparser.add_argument(
        '-c',
        '--conference',
        nargs='+',
        default="",
        help='pass conference need search')

    argparser.add_argument(
        '-n',
        '--number',
        default=None,
        help='number of paper need search')

    argparser.add_argument(
        '-y',
        '--year',
        default=None,
        help='pass year need search')

    args = argparser.parse_args()
    _main_(args)