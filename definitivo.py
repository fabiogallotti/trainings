# -*- coding: utf-8 -*-
"""
A simple Python script that takes some trainings from the web and upload them
to Google Calendar.

@author: Fabio
"""
from __future__ import print_function
from collections import defaultdict
import argparse
import datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

def parse_args():
    """
    Pass the url as argument.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Url to be scraped")
    parser.add_argument("-d", "--day", help="Starting day")
    parser.add_argument("-m", "--month", help="Starting month")
    parser.add_argument("-y", "--year", help="Starting year")
    args = parser.parse_args()
    return args

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
    data = defaultdict(dict)
    num_col = 1
    for row in table.find_all("tr"):
        col = row.find_all("td")
        num_day = 1
        try:
            for day in settimana[2:len(settimana)]:
                data[num_day][num_col] = col[num_day].text
                num_day += 1
            num_col += 1
        except IndexError:
            pass
    return data

def create_event(summary, start, day, week):
    """
    Create_event
    """
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    diff = datetime.timedelta(days=7*(week-1)+day-1)

    day = str((start + diff).date())
    event = {
        'summary': summary,
        'description': 'Creato da python',
        'start': {
            'date': day,
        },
        'end': {
            'date': day,
        },
    }
    return event

def upload(dati, d, m, y):
    """
    Upload the trainings to Google Calendar.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    start = datetime.date(year=y, month=m, day=d).isoformat()

    for day, weeks in dati.items():
        for week in weeks:
            event = create_event(dati[day][week], start, day, week)
            event = service.events().insert(calendarId='primary', body=event).execute()
            print("Event created: %s" % (event.get('htmlLink')))

if __name__ == '__main__':
    ARG = parse_args()
    trainings = extract(ARG.url)
    upload(trainings, int(ARG.day), int(ARG.month), int(ARG.year))

#trainingv2.py -u "https://www.repubblica.it/sport/running/schede/2016/11/24/news/mezza_maratone_km_21_097-152727929/" -d 27 -m 09 -y 2018
