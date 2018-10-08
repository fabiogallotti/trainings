# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 01:28:44 2018

@author: Fabio
"""

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

link  = "https://www.repubblica.it/sport/running/schede/2016/11/24/news/mezza_maratone_km_21_097-152727929/"
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
print("OBIETTIVO: " + settimana[0])


for row in table.find_all("tr"):
    col = row.find_all("td")
    try:
        for i in range(len(settimana)-1):
            print(settimana[i+1] + ": " + col[i].text)
        print("---")
    except IndexError:
        pass
