import requests


import execjs

# 读取并编译 JS
ctx = execjs.compile(open("code.js", encoding="utf-8").read())

password = "979269asx@"

# 调用 JS 函数
encrypted = ctx.call("toRSAcode", password)
print(encrypted)


login_headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Origin": "https://www.huangshan.com.cn",
    "Pragma": "no-cache",
    "Referer": "https://www.huangshan.com.cn/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "access-token": "null",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
login_url = "https://w.huangshan.com.cn/lotsapi/leaguer/api/userLeaguer/leaguerLogin"
login_params = {
    "loginName": "18063514542",
    "loginPass": encrypted,
    "merchantInfoId": "730"
}
response = requests.get(login_url, headers=login_headers, params=login_params)
leaguerId = response.json()["data"]["leaguerId"]
token = response.json()["data"]["token"]

print(leaguerId)
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Origin": "https://www.huangshan.com.cn",
    "Pragma": "no-cache",
    "Referer": "https://www.huangshan.com.cn/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "access-token": token,
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
url = "https://w.huangshan.com.cn/lotsapi/leaguer/api/userLeaguer/manage/leaguerInfo"
params = {
    "merchantInfoId": "730",
    "leaguerId": leaguerId
}
response = requests.get(url, headers=headers, params=params)

print(response.text)
