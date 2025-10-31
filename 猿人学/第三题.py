import requests
from collections import defaultdict

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://match.yuanrenxue.cn/match/3",
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
    "Hm_lvt_c99546cf032aaa5a679230de9a95c7db": "1733730479,1733732540,1734158623",
    "HMACCOUNT": "D839141A4A96109C",
    "tk": "-7343508528814843721",
    "sessionid": "9j9sqouu7pjj88bt15rkfvl5x4qm930c",
    "Hm_lvt_9bcbda9cbf86757998a2339a0437208e": "1733730481,1733732544,1734158634",
    "Hm_lpvt_9bcbda9cbf86757998a2339a0437208e": "1734158634",
    "Hm_lpvt_c99546cf032aaa5a679230de9a95c7db": "1734158638"
}
session = requests.session()
session.headers = headers
res = defaultdict(int)
for i in range(1, 6):
    url = "https://match.yuanrenxue.cn/jssm"
    response = session.post(url, cookies=cookies)

    url_p = 'https://match.yuanrenxue.cn/api/match/3?page={}'.format(i)
    resp = session.get(url=url_p, cookies=cookies)
    for data in resp.json()['data']:
        value = data['value']
        res[value] += 1
print(res)
print(dict(res))
print(max(res, key=lambda x: res[x]))
