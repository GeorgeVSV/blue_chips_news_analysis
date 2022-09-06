from bs4 import BeautifulSoup
import re
import json
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import nltk
#%matplotlib inline


# Get list of actual blue chips on stock market
base_url = 'https://investfunds.ru'
blue_chips_names = {}
blue_chips_url = 'https://investfunds.ru/stocks/?auto=1&limit=20'
response1 = requests.get(blue_chips_url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'})
html = BeautifulSoup(response1.text, 'lxml')
raw_chips = html.find('tbody')
hyperlinks_to_chips = raw_chips.find_all('a')
for link in hyperlinks_to_chips:
    chip_name = (re.sub(r'\,.*', "", link.text))
    blue_chips_names[chip_name] = (base_url + link.get('href'))



# Parse blue chips news (dates & titles)
chip_news = {}
for chip, chip_url in blue_chips_names.items():
    chip_news[chip] = {}
    chip_news[chip]['Dates'] = []
    chip_news[chip]['Titles'] = []
    response2 = requests.get(chip_url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'})
    html = BeautifulSoup(response2.text, 'lxml')
    raw_news = html.find('ul', class_='newsList')
    all_items = raw_news.find_all('li')

    for item in all_items:
        date = item.find('span').text.replace('|', '')
        chip_news[chip]['Dates'].append(date)
        title = item.find('b').text
        chip_news[chip]['Titles'].append(title)
        #print(date + '\n' + title)
        #chip_news['chip']['']


print((chip_news))



