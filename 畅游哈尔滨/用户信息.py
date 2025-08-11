import requests


headers = {
    "Accept": "application/json, text/javascript,",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json, text/javascript",
    "Referer": "https://servicewechat.com/wx156a2bf44f571c1d/22/page-frame.html",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
    "xweb_xhr": "1"
}
url = "https://ftcloud.bus365.com/bus/interface/useraction/userinfo"
params = {
    "deviceid": "1",
    "token": "{\"clienttype\":\"weixx\",\"clienttoken\":\"EEA495900A5892A6BE6B6D4B7936FD316F5C43E58836D88CB279B779538DE355AE21E8C8E3BC5E68F2CCD91743567FC40501629CBEBFDF379EDFC36BDB2336CD8EC23D1DA03DED2D5BD71E41E685559B2B8B65D65876F98BB0DB6C1BC44AF33415B18706ACF6AB39F00C542CD1BDE61296776C52AD2EEA860B0B828FD86779AB\",\"ordertoken\":\"\",\"version\":\"1.3.7.6\"}",
    "org": "88238482",
    "lang": "cn"
}
response = requests.get(url, headers=headers, params=params)

print(response.text)
print(response)