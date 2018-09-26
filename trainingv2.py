# -*- coding: utf-8 -*-
"""
A simple Python script that takes some trainings from the web and upload them
to Google Calendar.

@author: Fabio
"""
from __future__ import print_function
import argparse
import datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

def scrape():
    """
    Pass the url as argument.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="url to be scraped")
    args = parser.parse_args()
    return args.url

def extract(url):
    """
    Extract trainings from the web.
    """
    link = url
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})

    html = urlopen(req)
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")

    days = table.find_all("th")
    try:
        settimana = [days[i].text for i in range(len(days))]
    except IndexError:
        pass
    settimana[1] = "Settimana"
    data = dict()

    for row in table.find_all("tr"):
        col = row.find_all("td")
        cont = 1
        try:
            for elem in settimana[2:len(settimana)]:
                if elem in data:
                    data[elem] += col[cont].text
                else:
                    data[elem] = col[cont].text#+ ": " + col[elem].text + " "
                cont += 1
                #print("---")
        except IndexError:
            pass
        # for elem in settimana:
        #     if elem in data:
        #         data[elem] += col.text
        #     else:
        #         data[elem] = col.text

    print(data["Lunedi"])
    return 0

def upload():
    """
    Upload the trainings to Google Calendar.
    """

if __name__ == '__main__':
    URL = scrape()
    extract(URL)
#    upload()

#trainingv2.py -u "https://www.repubblica.it/sport/running/schede/2016/11/24/news/mezza_maratone_km_21_097-152727929/"
