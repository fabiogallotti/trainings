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
    parser.add_argument("--delete", action='store_true', default=False, help="Delete events")
    args = parser.parse_args()
    return args

def create_event(summary, start, day, week):
    """
    Create the event.
    """
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    diff = datetime.timedelta(days=7*(week-1)+day-1)

    day = str((start + diff).date())
    event = {
        'summary': summary,
        'description': 'Created using python',
        'start': {
            'date': day,
        },
        'end': {
            'date': day,
        },
    }
    return event

class Training:
    """
    Training.
    """
    def __init__(self, day, month, year, url=None):
        """
        Initialize a training object.
        """
        self.day = day
        self.month = month
        self.year = year
        self.url = url
        self.data = defaultdict(dict)

    def extract(self):
        """
        Extract trainings from the web.
        """
        req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req)
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table")
        days = table.find_all("th")
        try:
            week = [days[i].text for i in range(len(days))]
        except IndexError:
            pass
        num_col = 1
        for row in table.find_all("tr"):
            col = row.find_all("td")
            num_day = 1
            try:
                for day in week[2:len(week)]:
                    self.data[num_day][num_col] = col[num_day].text
                    num_day += 1
                num_col += 1
            except IndexError:
                pass

    def upload(self):
        """
        Upload the trainings to Google Calendar.
        """
        self.extract()
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()))

        start = datetime.date(year=self.year, month=self.month, day=self.day).isoformat()

        for day, weeks in self.data.items():
            for week in weeks:
                event = create_event(self.data[day][week], start, day, week)
                event = service.events().insert(calendarId='primary', body=event).execute()
                print("Event created: %s" % (event.get('htmlLink')))

    def delete(self):
        """
        Delete the events.
        """
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()))

        # Call the Calendar API
        now = datetime.datetime(year=self.year, month=self.month, day=self.day-1).isoformat() + 'Z'
        #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=100, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        for event in events:
            try:
                if event['description'] == 'Created using python':
                    eventId = event['id']
                    try:
                        service.events().delete(calendarId='primary', eventId = eventId).execute()
                        print("Event deleted.")
                    except:
                        print("Event not deleted.")
            except:
                pass

if __name__ == '__main__':
    ARG = parse_args()
    if ARG.delete:
        trainings = Training(int(ARG.day), int(ARG.month), int(ARG.year))
        trainings.delete()
    else:
        trainings = Training(int(ARG.day), int(ARG.month), int(ARG.year), ARG.url)
        trainings.upload()

#python trainings.py -u "https://www.repubblica.it/sport/running/schede/2016/11/24/news/mezza_maratone_km_21_097-152727929/" -d 03 -m 09 -y 2018
