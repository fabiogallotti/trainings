# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 01:28:44 2018

@author: Fabio
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup

link  = "https://www.repubblica.it/sport/running/schede/2016/11/24/news/mezza_maratone_km_21_097-152727929/"

html = urlopen(link)
soup = BeautifulSoup(html, "lxml")
table = soup.find("table")

settimana = ["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi", "Sabato", "Domenica"]

for row in table.find_all("tr"):
    col = row.find_all("td")
    try:  
        print("Settimana: " + col[0].text)
        for i in range(7):
            print(settimana[i] + ": " + col[i+1].text)
        print("---")
    except IndexError:
        pass