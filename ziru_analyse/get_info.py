# -*- coding:utf-8 -*-
import pymongo
from bs4 import BeautifulSoup
import requests
import time
import multiprocessing

#需要爬取得信息：
#标题 价格 位置 roomtag information 房屋配置 室友

client = pymongo.MongoClient('localhost',27017)
ziruProject = client['ziruProject']
urlListMongo = ziruProject['urlListMongo']
ziruInfo = ziruProject['ziruInfo']




def dealInfo(urllistRest):
    for i in urllistRest:
        time.sleep(0.5)
        print ('正在处理'+ i)
        print(i)
        web_data = requests.get(i)
        Soup = BeautifulSoup(web_data.text,'lxml')
        noPage = Soup.select('head script')
        try:
            if noPage[0].text.split('/')[2].split('.')[0] == 'noRoom':
                print ('已出租')
        except:
            print('处理中')
            roomName = Soup.select('div.room_name h2')

            roomLocal = Soup.select('div.room_name p.pr')
            locallist = [roomLocal[0].text.strip().split('￥')[0].split(']')[0][1:],\
                         roomLocal[0].text.strip().split('￥')[0].split(']')[1].strip()]

            roomPrice = roomLocal[0].text.strip().split('￥')[1].split('(')[0]

            roomDetail = Soup.select('ul.detail_room li')
            roomDetailList = []
            for item in roomDetail:
                if len(item.text.strip().split('\n')) ==1 :
                    roomDetailList.append(item.text.strip().split('\n')[0])
                elif  1<len(item.text.strip().split('\n')) <3:
                    roomDetailList.append([item.text.strip().split('\n')[0],item.text.strip().split('\n')[1].strip()])
                else:
                    roomDetailList.append(item.text.strip().split('\n'))

            roomAllo = Soup.select('ul.configuration.clearfix li')
            alloList= []
            for item in roomAllo:
                alloList.append(item.text)

            roomMateWoman = Soup.select('div.greatRoommate li.woman')
            roomMateMan = Soup.select('div.greatRoommate li.man')
            ziruInfo.insert_one({
                'url':i,
                'roomname':roomName[0].text.strip(),
                'locallist':locallist,
                'price':roomPrice,
                'roomDetail':roomDetailList,
                'roonAllo':alloList,
                'Womanmate':len(roomMateWoman),
                'manMate':len(roomMateMan),
                'totalroommate':len(roomMateWoman)+len(roomMateMan)
            })

def multcore():
    db_urls = set([item['url'] for item in urlListMongo.find()])
    info_urls = set([item['url'] for item in ziruInfo.find()])
    restUrl = list(db_urls - info_urls)
    sliceURl = len(restUrl)//4
    print(sliceURl)
    mps = []
    for i in range(4):
        mulDealList = restUrl[sliceURl*i:sliceURl*(i+1)]
        mp =  multiprocessing.Process(target=dealInfo,args=(mulDealList,))
        mp.start()
        mps.append(mp)
    [mp.join() for item in mps]

def mulPool():
    db_urls = set([item['url'] for item in urlListMongo.find()])
    info_urls = set([item['url'] for item in ziruInfo.find()])
    restUrl = list(db_urls - info_urls)
    sliceURl = len(restUrl) // 4
    pool = multiprocessing.Pool()


if __name__ =='__main__':
    multcore()