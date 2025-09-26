from pprint import pprint

import execjs
import requests
import json

from loguru import logger

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://www.swguancha.com",
    "Pragma": "no-cache",
    "Referer": "https://www.swguancha.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "deviceType": "1",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
url = "https://app.swguancha.com/client/v1/cPublic/consumer/baseInfo"
for page in range(1, 5):
    logger.info(f"第{page}页")
    data = {
        "size": 6,
        "current": page,
        "propertyCode": [
            "DISTRICT_PROP_GJ025_RJDQSCZZ",
            "DISTRICT_PROP_GJ117_NMSYGGQDCYYCLS",
            "DISTRICT_PROP_GJ001_NMHJRK"
        ],
        "dimensionTime": "2019",
        "levelType": 2
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, data=data)

    ctx = execjs.compile(open("decrypt.js", "r", encoding="utf-8").read())
    result = ctx.call("decrypt", response.text)

    print(result)