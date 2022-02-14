import requests
from bs4 import BeautifulSoup
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# Keywords that we need to match in th title 
keywords = ['medical devices', 'implantable', 'software as medical device', 
            'samd', 'mdufa', 'harmonised standards', 
            'medical device coordination group (mdcg)', 
            'combination product', 'guidance', 'notified body', 
            'artificial intelligence medical devices', 
            'artificial intelligence/machine learning-enabled medical devices',
            'machine learning-enabled medical devices',
            'artificial intelligence medical devices',
            'classification', 
            'designation', 'approval', 'recall', 'companion diagnostic', 
            'in vitro diagnostic (ivd)', 
            'device', 'software', 'health application', 'digital health', 
            'medical device regulation (mdr)', 'instruction for use (ifu)', 
            'medtech', 'unique device identification (udi)', '510(k)', 
            'investigational device exemption (ide)', 'de novo', 'premarket approval application (pma)', 
            'humanitarian device exemption (hde) ', 'device classification', 'iso', 'advamed', 'standard', 
            'eudamed', 'ce mark', 'declaration of conformity', 
            'general safety and performance requirements (gspr) ', 'european medicines agancy (ema)', 
            'european commission (ec)', 'eu reference laboratories (eurls)', 'eu expert panel', 
            'center for devices and radiological health (cdrh)', 'drug-device combination', 
            'national medical products administration (nmpa)', 
            'center for medical device evaluation (cmde)', 
            'medical device material', 'policy', 'swiss medtech']

'''
This is a utility function for formating the date
The format of date is : dd-mm-yyyy
return date in above format.
'''
def date_format(str1):
    '''
    l[0] = Month
    l[1] = Date
    l[2] = Year 
    '''
    str1 = str1.lower()
    l1 = str1.replace(',','').split(' ')
    # December -> dec
    if (len(l1[0]) > 3):
        l1[0] = l1[0][:3]
    dict1 = {'jan' : '01',
        'feb':'02',
        'mar':'03',
        'apr':'04',
        'may':'05',
        'jun':'06',
        'jul':'07',
        'aug':'08',
        'sep':'09',
        'oct':'10',
        'nov':'11',
        'dec':'12'
    }
    a = str(dict1[l1[0]])
    return str(l1[1].zfill(2)+'-'+ a +'-'+str(l1[2]))

'''
This is a utilty function for checking keywords in title.
This function returns a list of matched keywords, if any. 
Else it will retuern an empty list.
'''
def check_keywords_in_title(title, keywords):
    match = []
    for word in keywords:
        if word in title:
            # print(word, "matched for title :", title)
            match.append(word)
    return match

'''
Beautifulsoup for getting the page
'''
def getPage(url):
    try:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        req = session.get(url)
    except requests.exceptions.RequestException:
        return None
    return BeautifulSoup(req.text, 'html.parser')