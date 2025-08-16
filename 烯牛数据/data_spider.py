import random

import execjs
import json
import requests
import time

# JS 加密文件
with open("code.js", "r", encoding="utf-8") as f:
    js_code = f.read()
ctx = execjs.compile(js_code)

import requests
import json


headers = {
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "origin": "https://www.xiniudata.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.xiniudata.com/project/lib",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}
cookies = {
    "btoken": "R013OTC5U69WCXQN07AOJPKKMARY530C",
    "utoken": "E7L0DK7I4QCN2IJPNP0DONL6BUO00BB7",
    "username": "%E4%BA%91%E8%BE%B9%E5%B0%8F%E9%95%87",
    "Hm_lvt_42317524c1662a500d12d3784dbea0f8": "1753866077,1755249489,1755273939",
    "HMACCOUNT": "29C8E5B0264CE645",
    "Hm_lpvt_42317524c1662a500d12d3784dbea0f8": "1755273993"
}
url = "https://www.xiniudata.com/api/search3/company/search_company_for_lib"

s = {
    "industry_ids": 1659,
    "domestic": True,
    "corporate_locationIds": [],
    "tag_names": [],
    "corporate_rounds": [],
    "sort": 76006,
    "order": -1,
    "start": 20,
    "limit": 10
}

data = json.loads(ctx.call("encryptData", s))
data["v"] = 1
response = requests.post(url, headers=headers, cookies=cookies, json=data).json()
json_data = ctx.call("decryptData", response['d'])
company_code = [i['company_code'] for i in json_data['data']]

company_code_dit = {
    'codes': company_code
}
post_data = json.loads(ctx.call("encryptData", company_code_dit))
post_data["v"] = 1
link = 'https://www.xiniudata.com/api2/service/x_service/person_company4_list/list_companies4_list_by_codes'

link_json = requests.post(link, headers=headers, cookies=cookies, json=post_data).json()
json_data = ctx.call("decryptData", link_json['d'])
print(json_data)




