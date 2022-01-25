import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import urllib3
from datetime import date
from ais_utilities import date_format
from ais_utilities import check_keywords_in_title
from ais_utilities import keywords
from ais_utilities import getPage

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome import options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def getContent(url):
    print("Getting content for:- ", url)
    cookie_jar=requests.cookies.RequestsCookieJar()
    options = ChromeOptions()
    driver = Chrome(executable_path='C:/Users/nikhil/Downloads/chromedriver_win32/chromedriver.exe', options = options)
    driver.implicitly_wait(5)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    table = driver.find_elements_by_class_name("xmsonormal")
    for t in table:
        print(t.text)

def pacific(url):
    cookie_jar=requests.cookies.RequestsCookieJar()
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu') 
    driver = Chrome(executable_path='C:/Users/nikhil/Downloads/chromedriver_win32/chromedriver.exe', options = options)
    driver.implicitly_wait(0.5)
    driver.get('https://www.pacificbridgemedical.com/resource-center/?cat_resource_type%5B%5D=17&cat_resource_market=0&_type=')
    
    table = driver.find_elements_by_tag_name("article")
    all_news = []
    for t in table:
        news = {}
        title = t.find_element_by_class_name("entry-title").text.lower()
        url_content = t.find_element_by_tag_name("a").get_attribute('href')
        date1 = date_format(t.find_element_by_tag_name("time ").text)
        ret = check_keywords_in_title(title, keywords)
        print("Checking for:- ", title)
        if ret:
            print("Keyword matched.........")
            match = ""
            match = " | ".join(word for word in ret)
            print(match)
            news['identifier'] = url
            news['title'] = title
            news['url'] = url_content
            news['date'] = date1
            news['keywords'] = match
            all_news.append(news)
        else:
            print("\t No keywords matched.......")  
    for news in all_news:
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu') 
        driver = Chrome(executable_path='C:/Users/nikhil/Downloads/chromedriver_win32/chromedriver.exe', options = options)
        driver.implicitly_wait(5)
        wait = WebDriverWait(driver, 10)
        driver.get(news['url'])
        table = driver.find_elements_by_class_name("entry-content")
        content = ''
        print("Content pouplated............ for ",news['title'])
        for t in table:
            content += t.text
            news['content'] = content
    driver.close() 
    return all_news
