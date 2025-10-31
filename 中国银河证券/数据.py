from pprint import pprint

import requests

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "http://www.chinastock.com.cn/newsite/cgs-services/stockFinance/businessAnnc.html?type=marginList",
    "X-Requested-With": "XMLHttpRequest"
}

url = "http://www.chinastock.com.cn/website2020/doc/queryDocList"
for i in range(1, 4):
    params = {
        "pageSize": "50",
        "pageNo": i,
        "dayLimit": "9000",
        "catName": "yhgg_调整融资融券标的证券名单的公告",  # 直接写中文就行
        "startDate": "",
        "endDate": "",
        "stockCodeOrName": ""
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)

    pprint(response.json())
