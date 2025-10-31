# -*- coding: utf-8 -*-
# @Author   : HeLaoshi
# @File     : Codedemo1.py
# @Project  : pythonProject
import requests
import execjs  # pip install pyexecjs2

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://www.gaokao.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://www.gaokao.cn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Brave";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
page = 3
url = f'https://api.zjzw.cn/web/api/?is_single=2&local_province_id=43&page={page}&province_id=&request_type=1&size=10&special_id=4&top_school_id=1391&type=&uri=apidata/api/gk/special/school'

signsafe = execjs.compile(open('./CodeJSdemo2.js', 'r', encoding='utf-8').read()).call('main123', url)
print(signsafe)
json_data = {
    'is_single': 2,
    'local_province_id': '43',
    'page': 1,
    'province_id': '',
    'request_type': 1,
    'signsafe': signsafe,
    'size': 10,
    'special_id': '4',
    'top_school_id': '1391',
    'type': '',
    'uri': 'apidata/api/gk/special/school',
}
url = url + '&signsafe=' + signsafe
response = requests.post(url=url, headers=headers, json=json_data).json()
print(response)

