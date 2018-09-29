# -*- coding: utf-8 -*-
"""
A simple Python script that takes deletes events from Google Calendar.

@author: Fabio
"""
from __future__ import print_function
import argparse
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

def parse_args():
    """
    Pass the starting date.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--day", help="Starting day")
    parser.add_argument("-m", "--month", help="Starting month")
    parser.add_argument("-y", "--year", help="Starting year")
    args = parser.parse_args()
    return args

def delete(d, m, y):
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
    now = datetime.datetime(year=y, month=m, day=d-1).isoformat() + 'Z'
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=100, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    for event in events:
        try:
            if event['description'] == 'Creato da python':
                eventId = event['id']
                try:
                    service.events().delete(calendarId='primary', eventId = eventId).execute()
                    print("Evento cancellato")
                except:
                    print("Evento non cancellato")
        except:
            pass

if __name__ == '__main__':
    ARG = parse_args()
    delete(int(ARG.day), int(ARG.month), int(ARG.year))

#delete.py -d 3 -m 09 -y 2018
