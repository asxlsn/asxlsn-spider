import requests


headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://zph.fzrsrc.com",
    "Pragma": "no-cache",
    "Referer": "https://zph.fzrsrc.com/login/",
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
    "PHPSESSID": "09ff9c06ec396042260a92a3a37463f9",
    "PHPSESSID_NS_Sig": "oenCV6ibmTd2vgOz",
    "sl-session": "LNLKbr5Sl2ikg7EuvdeeHw==",
    "checkurl": "https%3A%2F%2Fzph.fzrsrc.com%2Findex.php%3Fm%3Dregister%26c%3Dok%26type%3D4"
}
url = "https://zph.fzrsrc.com/login/index.php"
params = {
    "c": "loginsave"
}
data = {
    "act_login": "0",
    "certificatetype": "1",
    "username": "513721200004050179",
    "password": "L6M5yboe8v7atGuA0EN6AHaBBjRbJIs9jdrxi0BdQmyfSMiWykIqU47l19/tH9ipFm1iTEyzun7SEuo697W9SQIX%2Bgxpd7zv4ykU1t9aDKy9FXflFMvcc1nsbEL6mvQGgvOBPtYXp0Ilb54Jyuv9Ils08Aqd8UHgwTfcr5A7JHM=",
    "loginname": "0",
    "authcode": "7988",
    "geetest_challenge": "",
    "geetest_validate": "",
    "geetest_seccode": ""
}
response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)

print(response.text)
print(response)