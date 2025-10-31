from pprint import pprint

import requests


headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.spiderdemo.cn/",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}
cookies = {
    "sessionid": "rlh8qae06qiyhpurbdadielyav3yptw7"
}
url = "https://www.spiderdemo.cn/admin_I/api/challenges"
response = requests.get(url, headers=headers, cookies=cookies)

challenges = response.json()
challenge = challenges['challenges']
for i in range(len(challenge)):
    print("题目列表:",i+1, challenge[i]['id'])




























