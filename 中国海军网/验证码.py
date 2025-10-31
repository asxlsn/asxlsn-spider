import base64


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
    "authToken": "beebb03b-1679-4bdb-b948-96370e93bea2",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
cookies = {
    "authToken": "beebb03b-1679-4bdb-b948-96370e93bea2"
}
url = "https://www.hjbwg.com/blueapi/api/user/imageValidateCode"
data = {}
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, cookies=cookies, data=data)

Image_Url= response.json()["data"]


def save_base64_image(base64_str, filename):
    # Base64 解码
    img_data = base64.b64decode(base64_str)
    # 写入 PNG 文件
    with open(filename, 'wb') as f:
        f.write(img_data)
    print(f"图片已保存: {filename}")

save_base64_image(Image_Url, "Image.png")



