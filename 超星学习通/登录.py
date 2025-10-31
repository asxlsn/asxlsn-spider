import execjs
import requests


headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://passport2.chaoxing.com",
    "Pragma": "no-cache",
    "Referer": "https://passport2.chaoxing.com/login?fid=&newversion=true&refer=https%3A%2F%2Fi.chaoxing.com",
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
    "JSESSIONID": "8E70625FA7ADCE97E45B131807A98804",
    "route": "fb0878d2b253f576b9614a77ccc901db",
    "retainlogin": "2",
    "fid": "10906",
    "source": "\"\""
}

with open("code.js", "r", encoding="utf-8") as f:
    js_code = f.read()
ctx = execjs.compile(js_code)
user_info = {
    "username": "13396450692",
    "password": "979269asx"
}

result = ctx.call("login", user_info.get("username"), user_info.get("password"))
url = "https://passport2.chaoxing.com/fanyalogin"
data = {
    "fid": "-1",
    "uname": result['phone'],
    "password": result['pwd'],
    "refer": "https://i.chaoxing.com",
    "t": "true",
    "forbidotherlogin": "0",
    "validate": "",
    "doubleFactorLogin": "0",
    "independentId": "0",
    "independentNameId": "0"
}
response = requests.post(url, headers=headers, cookies=cookies, data=data)

print(response.text)

