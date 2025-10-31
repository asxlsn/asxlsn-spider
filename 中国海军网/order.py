import requests
import json


headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "https://www.hjbwg.com",
    "Pragma": "no-cache",
    "Referer": "https://www.hjbwg.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "authToken": "c996f890-08e7-4ac5-b6a3-c6b6a0096799",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
cookies = {
    "authToken": "c996f890-08e7-4ac5-b6a3-c6b6a0096799"
}
url = "https://www.hjbwg.com/ticketapi/api/activityOrder/ck/addActivityOrder"
data = {
    "activityOrder": {
        "activityId": 8298,
        "liaisonPhone": "18030514542",
        "liaisonUser": "杨淮琳",
        "activityVisitDate": "2025-08-15",
        "activityVisitTime": "16:00-16:10"
    },
    "activityMemberList": [
        {
            "userName": "杨淮琳",
            "userIdCard": "513721200004050179",
            "userPhone": "",
            "userCertificateType": "ID_CARD",
            "ticketType": "VISIT_TICKET"
        }
    ],
    "validateCode": "4146"
}
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, cookies=cookies, data=data)

print(response.text)
print(response)