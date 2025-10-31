import base64
import requests
import ddddocr
import execjs
from PIL import Image
from io import BytesIO

# ========== 第一步：获取验证码 ==========
cookies = {
    'Hm_lvt_93f4034e873979432681a4780bea5b22': '1751354774,1751354807',
    'rc_sys': 'rc114',
    'Hm_lvt_57c48c2407b9363122624c39f3e251df': '1754572551',
    'HMACCOUNT': '29C8E5B0264CE645',
    'Hm_lpvt_57c48c2407b9363122624c39f3e251df': '1754572567',
    'ASP.NET_SessionId': 'fgpcxrveiele3gw5t030qnum',
    'returnUrl': 'http%3A%2F%2Fmember.rc114.com%3A804%2FUser%2FIndex',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'Hm_lvt_93f4034e873979432681a4780bea5b22=1751354774,1751354807; rc_sys=rc114; Hm_lvt_57c48c2407b9363122624c39f3e251df=1754572551; HMACCOUNT=29C8E5B0264CE645; Hm_lpvt_57c48c2407b9363122624c39f3e251df=1754572567; ASP.NET_SessionId=fgpcxrveiele3gw5t030qnum; returnUrl=http%3A%2F%2Fmember.rc114.com%3A804%2FUser%2FIndex',
    'Pragma': 'no-cache',
    'Referer': 'https://member.rc114.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}




# ========== 第一步：请求验证码并保存 ==========
resp = requests.get('https://member.rc114.com/Home/GetValidcode', cookies=cookies, headers=headers)
base64_url = resp.text.split('"ValidImage":"')[1].split('"}')[0]
image_data = base64.b64decode(base64_url)
img = Image.open(BytesIO(image_data))
img.save('验证码.png')

img_bytes_io = BytesIO()
img.save(img_bytes_io, format='PNG')
img_bytes = img_bytes_io.getvalue()

# ========== OCR识别点击坐标 ==========

ocr = ddddocr.DdddOcr(det=True, ocr=False)
ocr_result = ocr.detection(img_bytes)

print("ocr_result 原始数据：", ocr_result)

def center(box):
    x1, y1, x2, y2 = box
    cx = int((x1 + x2) / 2)
    cy = int((y1 + y2) / 2)
    return [cx, cy]

coords = [center(box) for box in ocr_result]
print("识别点击坐标:", coords)


# ========== JS生成 validateCode ==========

with open("captcha.js", "r", encoding="utf-8") as f:
    js_code = f.read()

ctx = execjs.compile(js_code)
validate_code = ctx.call("dealMapArr", coords)
print("生成 validateCode 参数:", validate_code)
