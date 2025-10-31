import time

import execjs
import requests



headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://match.yuanrenxue.cn/match/1",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "Hm_lvt_c99546cf032aaa5a679230de9a95c7db": "1732111613,1733660140",
    "HMACCOUNT": "E2B08AAFA947BE25",
    "Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3": "1732111754,1733660169",
    "Hm_lpvt_434c501fe98c1a8ec74b813751d4e3e3": "1733660189",
    "Hm_lvt_9bcbda9cbf86757998a2339a0437208e": "1733660230",
    "tk": "5754049163560447393",
    "sessionid": "1ogihcs1o94m9jri9szjzvtaoeoiw281",
    "Hm_lpvt_9bcbda9cbf86757998a2339a0437208e": "1733670754",
    "Hm_lpvt_c99546cf032aaa5a679230de9a95c7db": "1733670758"
}

with open('第一题.js', 'r',encoding='utf-8') as f:
    js_code = f.read()
ctx = execjs.compile(js_code)
m = ctx.call('encryptMD5')


url = "https://match.yuanrenxue.cn/api/match/1"
params = {
    "m": m
}
total = 0
num = 0
for page in range(1, 6):
    params = {
        "page": str(page),
        "m": m
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    if response.status_code == 200:
        print('请求第 {} 页结果：'.format(page), response.json())
        items = response.json()['data']
        for item in items:
            total += item['value']
        num += len(items)
    time.sleep(1)

print('所有机票价格的平均值: ', total / num)

