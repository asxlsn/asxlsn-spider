import base64
import requests
import ddddocr
import execjs
from PIL import Image
from io import BytesIO
import binascii
from gmssl import sm2

# ---------- 配置 ----------
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://member.rc114.com",
    "Pragma": "no-cache",
    "Referer": "https://member.rc114.com/",
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
    "Hm_lvt_93f4034e873979432681a4780bea5b22": "1751354774,1751354807",
    "rc_sys": "rc114",
    "Hm_lvt_57c48c2407b9363122624c39f3e251df": "1754572551",
    "HMACCOUNT": "29C8E5B0264CE645",
    "Hm_lpvt_57c48c2407b9363122624c39f3e251df": "1754572567",
    "ASP.NET_SessionId": "fgpcxrveiele3gw5t030qnum",
    "returnUrl": "http%3A%2F%2Fmember.rc114.com%3A804%2FUser%2FIndex"
}
captcha_url = 'https://member.rc114.com/Home/GetValidcode'
login_url = 'https://member.rc114.com/User/LoginForm'
js_file = 'captcha.js'  # 你的JS文件路径

public_key = "04CF18973EA8F51C60B5595D728BE3342B802E9275B34BCFC2B69E39099F5E624049C492FFF7FB1DCD9C999F29D26AC7121F438DE0F959AF49F8A92C9F3C11D4BB"  # 示例公钥
username = "18063514542"
password = "111111"
screen_dpi = "1536 × 864"
return_url = "http://member.rc114.com:804/User/Index"



# ---------- 辅助函数 ----------
def center(box):
    xs = box[0::2]
    ys = box[1::2]
    cx = int(sum(xs) / 4)
    cy = int(sum(ys) / 4)
    return [cx, cy]

def sm2_encrypt(data: str, public_key: str, cipher_mode: int = 0) -> str:
    if public_key.startswith('04'):
        public_key = public_key[2:]
    if len(public_key) != 128:
        raise ValueError("公钥长度不对")
    full_public_key = '04' + public_key
    data_bytes = data.encode('utf-8')
    sm2_crypt = sm2.CryptSM2(public_key=full_public_key, private_key='')
    encrypted_bytes = sm2_crypt.encrypt(data_bytes)
    encrypted_hex = binascii.b2a_hex(encrypted_bytes).decode().upper()
    if cipher_mode == 0:
        c1 = encrypted_hex[:130]
        c3 = encrypted_hex[-64:]
        c2 = encrypted_hex[130:-64]
        encrypted_hex = c1 + c3 + c2
    return '04' + encrypted_hex

# ---------- 获取验证码图片与提示文字 ----------
def get_captcha():
    resp = requests.get(captcha_url, cookies=cookies, headers=headers)

    json_data = resp.json()
    valid_text = json_data.get("ValidText")
    valid_image_base64 = json_data.get("ValidImage")
    with open('验证码.png', 'wb') as f:
        f.write(base64.b64decode(valid_image_base64))
    image_data = base64.b64decode(valid_image_base64)
    return valid_text, image_data

# ---------- OCR识别坐标 ----------

def center(box):
    x1, y1, x2, y2 = box
    cx = int((x1 + x2) / 2)
    cy = int((y1 + y2) / 2)
    return [cx, cy]





import ddddocr
from PIL import Image
from io import BytesIO

def ocr_coords_full_recognition(image_data, valid_text):
    print("开始OCR识别...")

    # 检测实例（只检测位置）
    ocr_det = ddddocr.DdddOcr(det=True, ocr=False)
    # 分类实例（只识别字符）
    ocr_cls = ddddocr.DdddOcr(det=False, ocr=True)

    img = Image.open(BytesIO(image_data))

    # 获取检测框
    ocr_result = ocr_det.detection(image_data)
    if not ocr_result or not isinstance(ocr_result, list):
        raise TypeError("OCR未检测到任何内容")

    print(f"检测到 {len(ocr_result)} 个字符框")

    # 按横向排序
    boxes_sorted = sorted(ocr_result, key=lambda box: box[0])

    char_positions = {}

    for idx, box in enumerate(boxes_sorted):
        # 裁剪字符框
        cropped = img.crop(box).resize((40, 40))
        bio = BytesIO()
        cropped.save(bio, format="PNG")
        crop_bytes = bio.getvalue()

        # 识别字符
        char = ocr_cls.classification(crop_bytes).strip()
        print(f"框 {idx} 识别结果: '{char}'")

        # 过滤条件：单个字符 + 在 valid_text 中 + 没选过
        if len(char) == 1 and char in valid_text and char not in char_positions:
            cx = (box[0] + box[2]) // 2
            cy = (box[1] + box[3]) // 2
            char_positions[char] = [cx, cy]
            print(f"✅ 匹配成功: '{char}'，坐标: {[cx, cy]}")
        else:
            print(f"❌ 不匹配或重复: '{char}'")

    # 按 valid_text 顺序返回
    coords = []
    for ch in valid_text:
        if ch in char_positions:
            coords.append(char_positions[ch])
        else:
            print(f"⚠ 警告: 未找到字符 '{ch}'")

    print(f"\n匹配坐标结果: {coords}")
    return coords







# ---------- 调用JS生成 validateCode ----------
def generate_validate_code(coords):
    with open(js_file, "r", encoding="utf-8") as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)
    return ctx.call("dealMapArr", coords)

# ---------- 登录请求 ----------
def login(validate_code, encrypted_pwd):
    data = {
        "userName": username,
        "pwdEncrypt": encrypted_pwd,
        "screenDpi": screen_dpi,
        "returnUrl": return_url,
        "validateCode": validate_code
    }
    response = requests.post(login_url, headers=headers, cookies=cookies, data=data)
    print("登录响应:", response.text)
    return response

# ---------- 主流程 ----------
def main():
    print("开始获取验证码...")
    valid_text, image_data = get_captcha()
    print("验证码提示文字:", valid_text)

    print("开始OCR识别...")
    coords = ocr_coords_full_recognition(image_data, valid_text)
    print("坐标:", coords)

    print("生成 validateCode 参数...")
    validate_code = generate_validate_code(coords)
    print("validateCode:", validate_code)

    print("加密密码...")
    encrypted_pwd = sm2_encrypt(password, public_key, cipher_mode=0)
    print("加密密码:", encrypted_pwd)

    print("开始登录...")
    login(validate_code, encrypted_pwd)

if __name__ == "__main__":
    main()
