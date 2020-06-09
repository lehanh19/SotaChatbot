from bs4 import BeautifulSoup
import requests
import argparse
import time
import os
import sys


def CreateURl(Conference="", Keywork="", Year=None):
    urlparser_first = 'https://arxiv.org/search/?query='
    urlparser_last = '&searchtype=all&source=header'
    if Year is not None:
        Year = str(Year)
    else:
        Year = ""
    if Conference is None:
        Conference = ""
    if Keywork is None:
        Keywork = ""
    Conference = Conference.strip()
    Keywork = Keywork.strip()
    Year = Year.strip()
    conference = Conference.replace(" ", "+")
    new_keywork = Keywork.replace(" ", "+")
    year = Year
    url_ = urlparser_first + "+" + new_keywork + "+" + conference + "+" + year + "+" + urlparser_last
    if Conference + Keywork + Year == "":
        return None
    else:
        return url_


def CrawlPaper(num_of_paper=None, url=None):
    ans = []
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'lxml')
    except OSError:
        ans.append('cannot open your requests URL, maybe something wrong. Please check again !')
        return ans
    all_paper = soup.find_all("li", {"class": "arxiv-result"})
    if len(all_paper) is 0:
        ans.append("Sorry!. Your query has no results.")
        return ans
    maxsize = len(all_paper)
    if num_of_paper != None:
        maxsize = min(int(num_of_paper),maxsize)
    # print("number of paper need search {} and size of list paper {}".format(num_of_paper, len(all_paper)))

    for index, paper in enumerate(all_paper):
        if index >= maxsize:
            return ans
        s = "Câu trả lời số " + str(index + 1) + ": " + paper.find('p', {"class": "title is-5 mathjax"}).text.replace("\n", "").strip() + "\n"
        s += paper.find('p', {"class": "authors"}).text.replace("\n", "").strip() + "\n"
        s += paper.find('p', {"class": "abstract mathjax"}).text.replace("\n", "").replace(" △ Less","").replace(" ▽ More ","").strip() + "\n"
        
        for link in paper.find_all("a"):
            if link.get('href'):
                if link['href'].split('/')[-2] == 'pdf':
                    s += "Link paper: " + link['href'] + "\n"  
                if link['href'].split("/")[-2] == 'abs':
                    s += "Link Summary paper: " + link['href'] + "\n"
        ans.append(s)
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

def _main_(args):
    if __name__ == '__main__':
        keyword_search = ' '.join(args.keyword)
        conference_search = ' '.join(args.conference)
        year_search = args.year
        num_of_paper = args.number_of_paper
# crawl paper
        print(" crawling paper ...............")
        time.sleep(5)
        url_origin = CreateURl(Conference=conference_search, Keywork=keyword_search, Year=year_search)
        print(url_origin)
        CrawlPaper(num_of_paper=num_of_paper, url=url_origin)
# crawl trending in github.com/trending
        print("crawling trend/github................")
        time.sleep(5)
        ans = Trending_github('https://github.com/trending/python?since=monthly',50).split("\n")
        for item in ans:
            print(item)
# crawl trending in paper with code
        print("crawling trend paper with code............................")
        time.sleep(5)
        ans = Trending_paperwithcode('https://paperswithcode.com/search?q_meta=&q=trending', 100).split("\n")
        for item in ans:
            print(item)
# crawl conference
        print("crawling conference .............................")
        time.sleep(5)
        ans = crawl_conference('http://www.guide2research.com/topconf/',number_of_conference = 6).split("\n")
        for item in ans:
            print (item)

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
        '--number_of_paper',
        default=None,
        help='number of paper need search')

    argparser.add_argument(
        '-y',
        '--year',
        default=None,
        help='pass year need search')

    args = argparser.parse_args()
    _main_(args)