# -*- coding:utf-8 -*-
from get_info import ziruInfo,urlListMongo
import time

while True:
    time.sleep(5)
    print('一共处理了：'+str(ziruInfo.find().count())+'信息')
    print('一共有：' + str(urlListMongo.find().count()) + '信息')