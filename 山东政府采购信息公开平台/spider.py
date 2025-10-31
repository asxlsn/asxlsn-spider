import requests
import json


headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "http://www.ccgp-shandong.gov.cn",
    "Pragma": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}
url = "http://sdgp.sdcz.gov.cn:8087/api/website/supp/getList"
data = {
    "currentPage": 2,
    "pageSize": 10,
    "suppName": "",
    "homePage": 1
}
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, data=data, verify=False)

print(response.text)
