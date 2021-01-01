from RunSQL import RunSQL
import requests
from time import sleep
import asyncio
import aiohttp
import os
import sys

rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
responseList = {}
async def async_http_call(row):
    try:
        #print('[ip] ' + row['ip'])
        url = 'http://' + row['ip']
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=1) as res:
                #print('req :: ' + str(row['seq']) + ' status : ' + str(res.status))
                if res.status >= 200 and res.status <= 399:
                    responseList[row['seq']] = 'Y'
                else:
                    responseList[row['seq']] = 'E'

    except Exception as e:
        #print('errMsg :: ' + str(e))
        responseList[row['seq']] = 'N'

async def process_async(page, rowCnt):
    json = {'rowcnt': rowCnt, 'offset': (page-1)*rowCnt}
    rows = RunSQL.selectList(json, 'getIptable.sql')

    tasks = [async_http_call(row) for row in rows]

    await asyncio.wait(tasks)

def sendSlack(cnt, key):
    slackUrl = 'https://hooks.slack.com/services/' + key
    data = {
        'channel': '#notification',
        'username': 'Notifier',
        'text': str(cnt)+'건 수집완료',
        'icon_emoji': 'sunglasses'
    }
    response = requests.post(slackUrl, json=data)
    #print(response.status_code)

args = sys.argv
firstPage = int(args[1])
lastPage = int(args[2])
slackKey = args[3]
rowCnt = 100
totalCnt = (lastPage - firstPage + 1) * rowCnt

if firstPage == None or lastPage == None:
    exit(1)

#full count : 1121513121
for page in range(firstPage, lastPage+1):
    print('page : ' + str(page)+'/'+str(lastPage) +' ::: start')
    asyncio.run(process_async(page, rowCnt))
    for key in responseList.keys():
        param = {'seq': key, 'check': responseList[key]}
        #print(param)
        RunSQL.save(param, 'update_iptable.sql')
    responseList = {}
    print('page : ' + str(page)+'/'+str(lastPage) +' ::: end')
    sleep(1)

sendSlack(totalCnt, slackKey)
print('complete')


