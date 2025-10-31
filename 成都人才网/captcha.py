import ddddocr
import execjs
import base64
import requests
from io import BytesIO
from PIL import Image

# 初始化OCR
ocr = ddddocr.DddOcr()

# 读取验证码图片 - 这里以网络图片为例
img_url = 'https://example.com/captcha.jpg'  # 替换为实际图片URL
resp = requests.get(img_url)
img = Image.open(BytesIO(resp.content))

# OCR识别文字和坐标
res = ocr.detect(img)

# 计算文字中心坐标
def get_center(box):
    xs = [p[0] for p in box]
    ys = [p[1] for p in box]
    cx = int(sum(xs) / 4)
    cy = int(sum(ys) / 4)
    return cx, cy

points = []
for item in res:
    cx, cy = get_center(item['box'])
    points.append([cx, cy])

print('识别到坐标:', points)





# 调用JS函数生成validateCode
validate_code = ctx.call('dealMapArr', points)
print('生成的 validateCode:', validate_code)

# TODO: 将validate_code放入登录请求参数中提交
