import time

import execjs
import requests
import json

data = {
    "pageNo": 1,
    "pageSize": 20,
    "total": 3268,
    "AREACODE": "",
    "M_PROJECT_TYPE": "",
    "KIND": "GCJS",
    "GGTYPE": "1",
    "PROTYPE": "",
    "timeType": "6",
    "BeginTime": "2025-03-26 00:00:00",
    "EndTime": "2025-09-26 23:59:59",
    "createTime": "",
    "ts": int(time.time())*1000,
}

data_for_sign = {k: v for k, v in data.items() if v not in ("", None)}
ctx = execjs.compile(open("code.js", "r", encoding="utf-8").read())
sign = ctx.call("d", data_for_sign)


headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://ggzyfw.fj.gov.cn",
    "Pragma": "no-cache",
    "Referer": "https://ggzyfw.fj.gov.cn/business/list/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "portal-sign": sign,
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
url = "https://ggzyfw.fj.gov.cn/FwPortalApi/Trade/TradeInfo"

data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, data=data).json()['Data']

decrypt_data = ctx.call("b", response)
print(decrypt_data)
