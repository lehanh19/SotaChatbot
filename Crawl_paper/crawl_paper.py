import argparse
import os
import sys
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import urllib.request


def CreateURl(Conference="", Keywork="", Year=None):
    urlparser_first = 'https://arxiv.org/search/?query='
    urlparser_last = '&searchtype=all&source=header'
    if Year is not None:
        Year = str(Year)
    else:
        Year = ""
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
    try:
        session = HTMLSession()
        resparvix = session.get(url)
        resparvix.html.render()
    except OSError:
        print('cannot open your requests URL, maybe something wrong. Please check again !')
        return
    session = HTMLSession()
    resparvix = session.get(url)
    resparvix.html.render()
    if len(resparvix.html.find(".arxiv-result")) is 0:
        print("Sorry!. Your query has no results.")
        return
    maxsize = len(resparvix.html.find(".arxiv-result"))
    if num_of_paper != None:
        maxsize = min(num_of_paper, len(resparvix.html.find(".arxiv-result")))
    for index, information in enumerate(resparvix.html.find(".arxiv-result")):
        if index >= maxsize:
            break
        print("Paper:{}. Title: {} \n ".format(index + 1, resparvix.html.find(".title")[index + 1].text))
        print(" {} \n".format(resparvix.html.find(".authors")[index].text))
        print(" {} \n".format(resparvix.html.find(".abstract")[index].text))
        for value in information.absolute_links:
            if value.split("/")[-2] == 'pdf':
                print("link pdf : {}".format(value))
            if value.split("/")[-2] == 'format':
                print("Summary paper: {}".format(value))
        print("==================================================")


def _main_(args):
    keyword_search = args.keyword
    conference_search = args.conference
    year_search = args.year
    num_of_paper = args.number_of_paper
    url_origin = CreateURl(Conference=conference_search, Keywork=keyword_search, Year=year_search)
    print(url_origin)
    CrawlPaper(num_of_paper=num_of_paper, url=url_origin)



if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='test crawl paper')

    argparser.add_argument(
        '-k',
        '--keyword',
        default="",
        help='pass keyword')

    argparser.add_argument(
        '-c',
        '--conference',
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