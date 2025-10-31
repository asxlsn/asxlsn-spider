import base64

import requests

import ddddocr

ocr = ddddocr.DdddOcr()

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "0",
    "Origin": "https://dxzhgl.miit.gov.cn",
    "Pragma": "no-cache",
    "Referer": "https://dxzhgl.miit.gov.cn/dxxzsp/xkz/xkzgl/resource/qiyesearch.jsp?num=%25E9%2599%2595%25E8%25A5%25BF%25E7%259B%259B%25E5%25AE%2589%25E5%258D%259A%25E4%25BF%25A1%25E9%2580%259A%25E8%25AE%25AF%25E6%259C%258D%25E5%258A%25A1%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8&type=xuke",
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
    "jsessionid": "rBQWfxroaNijIiy9tSk9CUuzgu7J2uKeICUA",
    "route": "1758990262.48.628.868813",
    "wzws_sessionid": "gTc2NzVkNYIwYWY0YjKAMTI1LjcwLjE4LjI1MqBo2KMi"
}
url = "https://dxzhgl.miit.gov.cn/dxxzsp/corpinfo/getCode"
params = {
    "0.485898003633664": ""
}
image = requests.post(url, headers=headers, cookies=cookies, params=params).json()['src']

head,context=image.split(",")  # 将base64_str以“,”分割为两部分
img_data = base64.b64decode(context)
with open("Code_image.png", "wb") as f:
    f.write(img_data)

with open("Code_image.png", "rb") as f:
    image_bytes = f.read()


result = ocr.classification(image_bytes)

# 输出识别结果
print(f"识别结果: {result}")
