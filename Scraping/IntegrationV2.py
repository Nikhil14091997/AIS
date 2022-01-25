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

# https://www.mddionline.com/regulatory-quality/regulations
def scrape_mddionline(url):
    cookie_jar=requests.cookies.RequestsCookieJar()
    session=requests.Session()
    header = {'Accept-Encoding': 'gzip, deflate', 'Accept': '/', 'Connection': 'keep-alive',
     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"
    }
    all_news=[]
    try:
        print("Utility function for https://www.mddionline.com/regulatory-quality/regulations called !")
        bs = getPage(url)
        
        table = bs.find_all('article', attrs={'class':'article-teaser article-teaser__icon__article article-teaser__aside'})
        for row in table:
            title = row.find('a').text.lower()
            url_content = row.find('a')['href']
            date = date_format(row.find('span').text.lstrip().rstrip())
            news = {}
            news['identifier'], news['title'], news['url'], news['date'], news['keywords'], news['content'] =url, title, url_content, date, '', ''
            ret = check_keywords_in_title(title, keywords)
            print(title, "- Keywords matched are:- ", ret)
            if ret:
                match = ""
                match = " | ".join(word for word in ret)
                print(match)
                news['keywords'] = match
                url_inner = 'https://www.mddionline.com' + url_content
                bs_inner = getPage(url_inner)
                content_inner = bs_inner.find('div', {'itemprop':'articleBody'})
                news['content'] = content_inner.text.lstrip()
                print("\t News content should be populated !")
                all_news.append(news)
            else:
                
                print("\t No Key Match, news content should not be populated !")
            all_news.append(news)
    except:
        print("An exception occured with:- ", url)
    return all_news
              
             


# https://www.ema.europa.eu
def scrapeEuropa(url):
    cookie_jar=requests.cookies.RequestsCookieJar()
    session=requests.Session()
    header = {'Accept-Encoding': 'gzip, deflate', 'Accept': '/', 'Connection': 'keep-alive',
     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"
    }
    all_news=[] 
    try:
        print("Utility function for https://www.ema.europa.eu called !")
        bs = getPage(url)
        table = bs.find('div', attrs = {'class':'view-content'})
        for row in table.findAll('a', attrs = {'class':'ecl-link ecl-list-item__link'}):
            news = {}
            news['identifier'] = url
            news['title'] = row.h3.text
            news['url']=row['href']
            news['date'] = row.span.text.replace("/","-")
            news['keywords'] = ''
            title, url_content, date, content = news['title'].lower(), news['url'], row.span.text ,''
            ret = check_keywords_in_title(title, keywords)
            print(title, "- Keywords matched are:- ", ret)
            if ret:
                match = ""
                match = " | ".join(word for word in ret)
                print(match)
                news['keywords'] = match
                url_inner = url + url_content
                bs_inner = getPage(url_inner)
                table_inner = bs_inner.find('div', attrs = {'class':'paragraphs-items paragraphs-items-field-ema-paragraph-content paragraphs-items-field-ema-paragraph-content-full paragraphs-items-full'})
                table_inner_1 = table_inner.find('div', attrs = {'class':'ecl-field__body'})
                table_inner_2 = table_inner_1.findAll('p')
                for i in table_inner_2:
                    content += i.get_text()
                news['content'] = content.replace("\n", " ")    
                print("\t News content should be populated !")
                all_news.append(news)
            else:
                print("\t No Key Match, news content should not be populated !")   
    except:
        print("An exception occured with:- ", url)
    return all_news



# https://www.fdanews.com/articles/topic/106?page=5
def scrapeFDA(url):
    all_news=[] 
    try:
        print("Utility function for https://www.fdanews.com called !")
        bs = getPage(url)
        # Checkpoint No. of records pulled is incorrect
        table = bs.findAll('article', attrs = {'class':'record article-summary'})
        for row in table:
            news = {}
            news['identifier'] = url
            news['title'], news['url'] = row.h2.text, row.h2.a['href']
            news['date'] = date_format(row.find('div' , attrs = {'class' : 'date article-summary__post-date'}).text)
            title, url_content, date, content = news['title'].lower(), news['url'], news['date'],''
            ret = check_keywords_in_title(title, keywords)
            news['keywords'] = ''
            print("check_keywords_in_title called for title:- ", title)
            if ret:
                match = ""
                match = " | ".join(word for word in ret)
                print("\t Found a keyword!!")
                news['keywords'] = match
                url_inner = url_content
                time.sleep(2)
                bs_inner = getPage(url_inner)
                table_inner = bs_inner.find('div', attrs = {'body gsd-paywall'})
                table_inner_1 = table_inner.findAll('p')
                for i in table_inner_1:
                    content += i.get_text()
                news['content'] = content.replace("\n", " ") 
                all_news.append(news)
                print("\t News content should be populated !")
                
            else:
                print("\t No Key Match, news content should not be populated !")
        time.sleep(2)
    except:
        print("An exception occured with:- ", url)
    return all_news


# https://www.medtechdive.com/topic/medical-devices/
def scrapeMedTechDive(url):
    all_news=[] 
    cookie_jar=requests.cookies.RequestsCookieJar()
    session=requests.Session()
    header = {'Accept-Encoding': 'gzip, deflate', 'Accept': '/', 'Connection': 'keep-alive',
     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"
     }
    try:   
        print("Utility function for https://www.medtechdive.com/topic/medical-devices/ called !")
        bs = getPage(url)
        all_news=[] 
        table = bs.find('ul', attrs = {'class':'feed layout-stack-xxl'})
        for row in table.findAll('div', attrs = {'class':'medium-8 columns'}):
            news = {}
            news['identifier'] = url
            news['title'] = row.h3.text.lstrip().rstrip()
            news['url']=row.a['href']
            dummy = row.findAll('span', attrs ={'class':'secondary-label'})[-1]
            dummy = dummy.text.lstrip().rstrip().replace(",", "")
            date = dummy.split(" ")[-3:]
            date = ' '.join(date)
            news['date'] = date_format(date)
            news['keywords'] = ''
            title, url_content, date, content = news['title'].lower(), news['url'], news['date'] ,''
            ret = check_keywords_in_title(title, keywords)
            print(title, "- Keywords matched are:- ", ret)
            if ret:
                match = " "
                match = " | ".join(word for word in ret)
                print(match)
                news['keywords'] = match
                #print("\t Found a keyword!!")
                base_url = "https://www.medtechdive.com"
                url_inner = base_url + url_content
                time.sleep(4)
                bs_inner = getPage(url_inner)
                table_inner = bs_inner.find('div', attrs = {'class':'large medium article-body'})
                table_inner_1 = table_inner.findAll('p')
                for i in table_inner_1:
                    content += i.get_text()
                news['content'] = content.replace("\n", " ") 
                all_news.append(news)
                print("\t News content should be populated !")
            else:
                print("\t No Key Match, news content should not be populated !") 
        time.sleep(2)
    except:
        print("An exception occured with:- ", url)
    return all_news

# https://www.raps.org/news-and-articles/news-articles
def scrapeRaps(url):
    all_news = []
    cookie_jar=requests.cookies.RequestsCookieJar()
    session=requests.Session()
    header = {'Accept-Encoding': 'gzip, deflate', 'Accept': '/', 'Connection': 'keep-alive',
     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"
     }
    try:
        print("Utility function for https://www.raps.org/news-and-articles/news-articles called !")
        req = requests.get(url, headers = header)
        soup=BeautifulSoup(req.content, "html.parser")
        newsList = soup.findAll("div", {"class": "item-content"})
        for eachNews in newsList:
            news = {}
            news['identifier'] = url
            url_content=eachNews.a['href']
            title = eachNews.a.text.strip().lower()
            date = eachNews.li.text
            date1 = date.split(" ")
            date = date1[1] + " " + date1[0] + " " + date1[2]
            news['title'] = title
            news['url'] = 'https://www.raps.org' + url_content
            news['date'] = date_format(date)
            news['keywords'] = ''
            ret = check_keywords_in_title(title, keywords)
            print(title, "- Keywords matched are:- ", ret)
            if ret:
                match = ""
                match = " | ".join(word for word in ret)
                print(match)
                news['keywords'] = match
                print("\t Found a keyword!!")
                req_inner = requests.get(news['url'], headers = header)
                soup_inner = BeautifulSoup(req_inner.content, "html.parser")
                table = soup_inner.find('div', attrs = {'class':'article'})
                row = table.findAll('div')[1]
                news['content'] = row.text
                all_news.append(news)
                print("\t News content should be populated !")
            else:
                print("\t No Key Match, news content should not be populated !")
            time.sleep(2)
    except:
        print("An exception occured with:- ", url)
    return all_news
    

 