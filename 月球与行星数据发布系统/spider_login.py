import execjs
import requests


headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://moon.bao.ac.cn",
    "Pragma": "no-cache",
    "Referer": "https://moon.bao.ac.cn/ce5web/searchOrder_dataSearchData.search",
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
    "JSESSIONID": "EA4E969D6E531CAEC0303A3C70FFB4A3",
    "COOKIE_SUPPORT": "true",
    "GUEST_LANGUAGE_ID": "zh_CN",
    "bianhao": "",
    "CE2CCD": "false",
    "sciTime": "2019-01-03/2019-01-03",
    "keyWordClickPath": "CE4/LCAM/level/2A"
}
url = "$https://moon.bao.ac.cn/ce5web/loginJsonAction\u0021loginValidateAjax.login"

with open("code.js", "r", encoding="utf-8") as f:
    js_code = f.read()
ctx = execjs.compile(js_code)
result = ctx.call("encodeCredentials", 18063514542, 111111)

data = {
    "username": result['usernameBase64'],
    "password": result['passwordBase64'],
}
print(data['username'])
print(data['password'])
response = requests.post(url, headers=headers, cookies=cookies, data=data)

print(response.text)