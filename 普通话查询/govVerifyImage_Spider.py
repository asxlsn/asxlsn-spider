# govVerifyImage_Spider.py
import base64
import requests
import ddddocr

def get_verify_code():
    """
    获取并识别验证码
    返回: 识别结果字符串
    """
    ocr = ddddocr.DdddOcr()

    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Origin": "https://zwfw.moe.gov.cn",
        "Pragma": "no-cache",
        "Referer": "https://zwfw.moe.gov.cn/mandarin/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "reqType": "3",
        "rn": "1760450435455",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sign": "bd5ae2e650bfe5d89c8cc0df55085fc3",
        "uid;": ""
    }

    cookies = {
        "_abfpc": "e04de75d72ef947532f3c7ed97eb967560e42291_2.0",
        "cna": "1a9e2a47231636ffc1133d4c115c32f8"
    }

    url = "https://zwfw.moe.gov.cn/eduSearch/prod/moe/govVerifyImage"
    response = requests.post(url, headers=headers, cookies=cookies).json()

    # 获取图像数据
    Image_data = response['data']['imageUrl']

    # 分离data URI前缀和实际的base64数据
    if ',' in Image_data:
        head, context = Image_data.split(",", 1)
    else:
        context = Image_data

    # 解码base64数据
    img_data = base64.b64decode(context)

    # 保存图像文件
    with open("Code_image.png", "wb") as f:
        f.write(img_data)

    # 读取图像进行OCR识别
    with open("Code_image.png", "rb") as f:
        image_bytes = f.read()

    result = ocr.classification(image_bytes)
    return result

# 保持原有功能，可以直接运行此脚本测试
if __name__ == "__main__":
    result = get_verify_code()
    print(f"识别结果: {result}")
