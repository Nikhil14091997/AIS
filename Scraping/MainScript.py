import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import urllib3
from datetime import date
from datetime import date
from ais_utilities import date_format
from ais_utilities import check_keywords_in_title
from ais_utilities import keywords
from ais_utilities import getPage
from pacific import getContent, pacific
from IntegrationV2 import scrapeEuropa, scrape_mddionline, scrapeFDA, scrapeMedTechDive, scrapeRaps
from IntegrationV2 import chinaMedDevice

dataHuggingFace = []

'''
Conatiner 1 : Websites that could be scraped without selenium: i.e. we do not need to  render 
javascript on browser for the websites to to produce data

Container 2 : We need to render the code on Javascript in a browser to get the data

'https://www.ema.europa.eu' - Container 1
'https://www.mddionline.com/regulatory-quality/regulations' - Container 1
'https://www.fdanews.com/articles/topic/106?page=5' - Container 1
'https://www.medtechdive.com/topic/medical-devices/' - Container 1
'https://www.raps.org/news-and-articles/news-articles' - Container 1
'https://www.pacificbridgemedical.com/resource-center/?cat_resource_type%5B%5D=17&cat_resource_market=0&_type=' - Container 2

'''


url = ['https://www.ema.europa.eu',
       'https://www.mddionline.com/regulatory-quality/regulations',
       'https://www.fdanews.com/articles/topic/106?page=5',
       'https://www.medtechdive.com/topic/medical-devices/',
       'https://www.raps.org/news-and-articles/news-articles',
       'https://www.pacificbridgemedical.com/resource-center/?cat_resource_type%5B%5D=17&cat_resource_market=0&_type=',
       "https://chinameddevice.com/cmd-blogs"
       ]
#Calling 'https://www.pacificbridgemedical.com/resource-center/?cat_resource_type%5B%5D=17&cat_resource_market=0&_type=' website's function
all_news = pacific(url[5])
if len(all_news) > 1:
    print("Data for:-", url[5], " populated successfully !!")

dataHuggingFace.append(all_news)

time.sleep(3)

# Calling 'https://www.ema.europa.eu' website's function
all_news = scrapeEuropa(url[0])
if len(all_news) > 1:
    print("Data for:-", url[0], " populated successfully !!")
dataHuggingFace.append(all_news)

time.sleep(2)

# Calling 'https://www.mddionline.com/regulatory-quality/regulations' website's function
all_news = scrape_mddionline(url[1])
if len(all_news) > 1:
    print("Data for:-", url[1], " populated successfully !!")
dataHuggingFace.append(all_news)

time.sleep(2)

# Calling 'https://www.fdanews.com/articles/topic/106?page=5' website's function
all_news = scrapeFDA(url[2])
if len(all_news) > 1:
    print("Data for:-", url[2], " populated successfully !!")
dataHuggingFace.append(all_news)

time.sleep(2)

# Calling 'https://www.medtechdive.com/topic/medical-devices/' website's function
all_news = scrapeMedTechDive(url[3])
if len(all_news) > 1:
    print("Data for:-", url[3], " populated successfully !!")
dataHuggingFace.append(all_news)

time.sleep(2)

# Calling 'https://www.raps.org/news-and-articles/news-articles' website's function
all_news = scrapeRaps(url[4])
if len(all_news) > 1:
    print("Data for:-", url[4], " populated successfully !!")
dataHuggingFace.append(all_news)

time.sleep(2)

# Calling 'https://chinameddevice.com/cmd-blogs' website's function
all_news = chinaMedDevice(url[6])
if len(all_news) > 1:
    print("Data for:-", url[6], " populated successfully !!")
dataHuggingFace.append(all_news)
print("Data Population in list of dictionaries")