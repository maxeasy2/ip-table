from RunSQL import RunSQL
import requests
from time import sleep
import asyncio
import aiohttp
import os
import sys
from bs4 import BeautifulSoup

rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
responseTitleList = {}
responseBodyList = {}
async def async_http_call(row):
    try:
        #print('[ip] ' + row['ip'])
        url = 'http://' + row['ip']
        #url = 'https://beomi.github.io/2017/01/20/HowToMakeWebCrawler/'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=1) as res:
                #print('req :: ' + str(row['seq']) + ' status : ' + str(res.status))
                if res.status >= 200 :
                    html = await res.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    title = soup.title.text
                    responseTitleList[row['seq']] = title
                    responseBodyList[row['seq']] = html
    except Exception as e:
        print('#')


async def process_async(page, rowCnt):
    json = {'rowcnt': rowCnt, 'offset': (page-1)*rowCnt}
    rows = RunSQL.selectList(json, 'getAccessIptable.sql')
    tasks = [async_http_call(row) for row in rows]
    await asyncio.wait(tasks)

def sendSlack(cnt, key):
    slackUrl = 'https://hooks.slack.com/services/' + key
    data = {
        'channel': '#notification',
        'username': 'Notifier',
        'text': str(cnt)+'건 타이틀 수집완료',
        'icon_emoji': 'sunglasses'
    }
    response = requests.post(slackUrl, json=data)
    #print(response.status_code)

args = sys.argv
firstPage = int(args[1])
lastPage = int(args[2])
slackKey = args[3]
rowCnt = 1
totalCnt = (lastPage - firstPage + 1) * rowCnt

if firstPage == None or lastPage == None:
    exit(1)

#full count : 1121513121
for page in range(firstPage, lastPage+1):
    print('page : ' + str(page)+'/'+str(lastPage) +' ::: start')
    asyncio.run(process_async(page, rowCnt))
    for key in responseTitleList.keys():
        param = {'seq': key, 'title': responseTitleList[key], 'html': responseBodyList[key]}
        print(param)
        RunSQL.save(param, 'insert_access_website.sql')
    responseTitleList = {}
    responseBodyList = {}
    print('page : ' + str(page)+'/'+str(lastPage) +' ::: end')
    sleep(1)

sendSlack(totalCnt, slackKey)
print('complete')


