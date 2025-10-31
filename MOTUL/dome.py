from pprint import pprint

import requests


headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.motul.com/zh-CN/lubricants",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "x-nextjs-data": "1"
}
url = "https://www.motul.com/_next/data/cmr3OC3iy9iN04JwpYBpG/zh-CN/lubricants/recommendations/89456.json"
params = {
    "vehicleTypeId": "89456"
}
response = requests.get(url, headers=headers, params=params)

pprint(response.json())