import execjs
import requests
import json
import time

from loguru import logger

with open('getSignCode.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

# 编译 JavaScript 代码
ctx = execjs.compile(js_code)

timestamp = str(int(time.time() * 1000))
# 调用 JavaScript 函数进行加密
encrypted_timestamp = ctx.call('encryptTimestamp', timestamp)
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Authorization": "xzxk_wbjg",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://xk.scjgj.sh.gov.cn",
    "Pragma": "no-cache",
    "Referer": "https://xk.scjgj.sh.gov.cn/xzxk_wbjg/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sign": encrypted_timestamp,
    "timestamp": timestamp
}
cookies = {
    "9402eb87-1f71-40f8-b765-13114c94d69d": "WyIxNzI2ODExOTMxIl0"
}
url = "https://xk.scjgj.sh.gov.cn/xzxk_wbjg/query/public/licInfo"
data = {
    "zszl": "00101,00102",
    "fzjg": "",
    "sqaid": "",
    "shxydm": "",
    "rows": 20,
    "page": 1
}
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, cookies=cookies, data=data)

logger.info(response.text)
