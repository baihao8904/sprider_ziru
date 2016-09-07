# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
ziruProject = client['ziruProject']
urlListMongo = ziruProject['urlListMongo']


host_url = 'http://www.ziroom.com'
for page in range(1,251):
    url = 'http://www.ziroom.com/z/nl/sub/z2.html?p={}'.format(str(page))
    print (url)
    web_data = requests.get(url)
    Soup = BeautifulSoup(web_data.text,'lxml')
    houseUrl = Soup.select('div.txt h3 a')
    for item in houseUrl:
        finalUrl = host_url + item.get('href')
        urlListMongo.insert_one({'url':finalUrl})
    time.sleep(2)
print('final')

