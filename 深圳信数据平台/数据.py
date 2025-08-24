import requests
import execjs
import json

import pandas as pd
EncKey = execjs.compile(open('code.js', 'r', encoding='utf-8').read()).call('getResCode')

headers = {
    "Accept": "*/*",
    "Accept-EncKey": "bX339fYwHfyPt7Fl72j4hg==",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://webapi.cninfo.com.cn",
    "Pragma": "no-cache",
    "Referer": "https://webapi.cninfo.com.cn/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
cookies = {
    "MALLSSID": "564F33715A6C33615037305A623151367042414B3175396D56774F3735686377307734366C6B6A4D682B6D7575505271396F77597357454249306B514F6F316A"
}
url = "https://webapi.cninfo.com.cn/api/sysapi/p_sysapi1007"
data = {
    "tdate": "2025-08-22",
    "market": "SZE"
}
response = requests.post(url, headers=headers, cookies=cookies, data=data)


# 增强版代码：添加异常处理
try:
    records = response.json().get('records', [])
    for item in records:
        交易所 = item.get('交易所', '')
        最低价 = item.get('最低价', '')
        币种 = item.get('币种', '')
        涨跌 = item.get('涨跌', '')
        最高价 = item.get('最高价', '')
        证券简称 = item.get('证券简称', '')
        开盘价 = item.get('开盘价', '')
        涨跌幅 = item.get('涨跌幅', '')
        成交金额 = item.get('成交金额', '')
        证券代码 = item.get('证券代码', '')
        成交数量 = item.get('成交数量', '')
        收盘价 = item.get('收盘价', '')
        print(交易所, 最低价, 币种, 涨跌, 最高价, 证券简称, 开盘价, 涨跌幅, 成交金额, 证券代码, 成交数量, 收盘价)
        # 将数据写入Excel文件
    df = pd.DataFrame(records)
    df.to_excel('深圳信.xlsx', index=False, engine='openpyxl')
    print("数据已成功写入深圳信.xlsx文件")
except (requests.RequestException, ValueError, KeyError) as e:
    print(f"数据处理出错: {e}")


