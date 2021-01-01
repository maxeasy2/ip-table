from RunSQL import RunSQL
import requests
from time import sleep


#full count : 1121513121
for page in range(25, 100000):
    print('page : ' + str(page))
    rowCnt = 100
    json = {'start': page * rowCnt, 'rowcnt': rowCnt}
    rows = RunSQL.selectList(json, 'getIptable.sql')

    for row in rows:
        try:
            print('[ip] ' + row['ip'])
            url = 'http://' + row['ip']
            req = requests.get(url, timeout=1)
            print('req :: ' + str(row['seq']) + ' status : ' + str(req.status_code))
            if req.status_code >= 200 and req.status_code <= 399:
                param = {'check': 'Y', 'seq': row['seq']}
            else:
                param = {'check': 'E', 'seq': row['seq']}
            RunSQL.save(param, 'update_iptable.sql')
        except Exception as e:
            print('errMsg :: ' + str(e))
            param = {'check': 'N', 'seq': row['seq']}
            RunSQL.save(param, 'update_iptable.sql')
    sleep(1)


slackUrl = 'https://hooks.slack.com/services/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'
data = {
    'channel': '#notification',
    'username': 'Notifier',
    'text': '100000건 수집완료',
    'icon_emoji': 'sunglasses'
}
requests.post(slackUrl, json=data)
