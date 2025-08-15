import random

import execjs
import json
import requests
import time

# JS 加密文件
with open("code.js", "r", encoding="utf-8") as f:
    js_code = f.read()
ctx = execjs.compile(js_code)

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://www.xiniudata.com",
    "referer": "https://www.xiniudata.com/industry/newest?from=data",
    "user-agent": "Mozilla/5.0"
}
cookies = {
    "btoken": "R013OTC5U69WCXQN07AOJPKKMARY530C"
}

url = "https://www.xiniudata.com/api2/service/x_service/person_industry_list/list_industries_by_sort"

page_size = 20
total_pages = 3  # 假设爬取前5页，可根据需要改

for page in range(total_pages):
    start = page * page_size
    payload_data = {
        "sort": 1,
        "start": start,
        "limit": page_size
    }

    # 调用 JS 加密 + 生成 sig
    result = ctx.call("generatePayloadAndSig", payload_data)
    f_val = result["payload"]
    sig_val = result["sig"]
    # 组装请求
    data = {
        "payload": f_val,
        "sig": sig_val,
        "v": 1
    }

    response = requests.post(url, headers=headers, cookies=cookies, data=json.dumps(data, separators=(',', ':')))
    print(f"第 {page + 1}页: response:")
    time.sleep(random.uniform(3, 5))#随机休眠3-5秒
    result = ctx.call("decrypt_data", response.json()['d'])
    print(result)

