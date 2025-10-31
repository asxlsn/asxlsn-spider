from pprint import pprint

import requests
import json


headers = {
    "authority": "wxapi.sports8.com.cn",
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/json",
    "referer": "https://servicewechat.com/wxd0286fb3b0e39384/105/page-frame.html",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
    "xweb_xhr": "1"
}
url = "https://wxapi.sports8.com.cn/api/ydb/stadium/apiGetSearchStadiumByWxapp"
data = {
    "userid": "",
    "cityid": "75",
    "date": 1756051200,
    "timePeriod": "6,23",
    "lat": 30.656179428100586,
    "lng": 104.08329010009766,
    "biz": "apiGetSearchStadiumByWxapp",
    "method": "WxAppBooking",
    "nonce": "2508201756106269338",
    "sign": "1736E387786710B5D4E59BDBE07C8693"
}
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, data=data).json()

pprint(response)
