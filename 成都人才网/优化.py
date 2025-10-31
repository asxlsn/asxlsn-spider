import base64
import requests
import ddddocr
import execjs
from PIL import Image
from io import BytesIO
import binascii
from gmssl import sm2
import time
import os

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
js_file = 'captcha.js'  # 可选，本地的 dealMapArr JS；若不存在将使用 Python 实现

public_key = "04CF18973EA8F51C60B5595D728BE3342B802E9275B34BCFC2B69E39099F5E624049C492FFF7FB1DCD9C999F29D26AC7121F438DE0F959AF49F8A92C9F3C11D4BB"
username = "18063514542"
password = "979269Asx@"
screen_dpi = "1536 × 864"
return_url = "http://member.rc114.com:804/User/Index"

# ---------- 辅助函数 ----------
def sm2_encrypt(data: str, public_key: str, cipher_mode: int = 0) -> str:
    """
    使用 gmssl 的 SM2 对 data 字符串进行加密，返回大写 hex 串（与网页端兼容的拼装）
    """
    if public_key.startswith('04'):
        public_key = public_key[2:]
    if len(public_key) != 128:
        raise ValueError("公钥长度不对，应该为128个Hex字符（除去起始的04）")
    full_public_key = '04' + public_key
    data_bytes = data.encode('utf-8')
    sm2_crypt = sm2.CryptSM2(public_key=full_public_key, private_key='')
    encrypted_bytes = sm2_crypt.encrypt(data_bytes)
    encrypted_hex = binascii.b2a_hex(encrypted_bytes).decode().upper()
    # 若后端/前端使用 c1+c3+c2 排列（常见做法），则按你原来的调整
    if cipher_mode == 0:
        # 130 = 65字节 * 2 hex char; c3 64 hex; c2 剩余
        c1 = encrypted_hex[:130]
        c3 = encrypted_hex[-64:]
        c2 = encrypted_hex[130:-64]
        encrypted_hex = c1 + c3 + c2
    return '04' + encrypted_hex

def save_image_bytes(image_bytes, path='验证码.png'):
    with open(path, 'wb') as f:
        f.write(image_bytes)

# ---------- 获取验证码图片与提示文字 ----------
def get_captcha(retries=3, sleep_sec=0.6):
    for attempt in range(retries):
        resp = requests.get(captcha_url, cookies=cookies, headers=headers, timeout=10)
        try:
            json_data = resp.json()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(sleep_sec)
                continue
            raise
        valid_text = json_data.get("ValidText")
        valid_image_base64 = json_data.get("ValidImage")
        if not valid_image_base64 or not valid_text:
            if attempt < retries - 1:
                time.sleep(sleep_sec)
                continue
            raise ValueError("未从接口获取到有效的 ValidImage/ValidText")
        image_data = base64.b64decode(valid_image_base64)
        save_image_bytes(image_data, '验证码.png')
        return valid_text, image_data
    raise RuntimeError("获取验证码失败（重试耗尽）")

# ---------- OCR识别坐标 （增强版，适配旧版 ddddocr） ----------
def ocr_coords_full_recognition(image_data, valid_text, max_click=4):
    """
    给定验证码图片的 bytes 和 valid_text（如 '穿房入户'），返回按顺序的点击坐标列表
    coords: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]] 长度等于 len(valid_text)（通常4）
    """
    print("开始 OCR 识别...")
    ocr_det = ddddocr.DdddOcr(det=True, ocr=False)
    ocr_cls = ddddocr.DdddOcr(det=False, ocr=True)

    img = Image.open(BytesIO(image_data))
    img_w, img_h = img.size

    boxes = ocr_det.detection(image_data)
    if not boxes or not isinstance(boxes, list):
        raise TypeError("OCR未检测到任何文本框")

    print(f"检测到 {len(boxes)} 个候选字符框")
    # boxes 的每个元素可能是 [x1,y1,x2,y2], 按 x 排序
    boxes_sorted = sorted(boxes, key=lambda b: b[0])

    char_positions = {}
    # 识别尝试策略：对每个 box 尝试多种 resize/扩边组合，直到得到单个字符
    resize_options = [(40,40), (56,56), (72,72)]
    pad_options = [0, -2, 2, -4, 4]  # 在 crop 边界上做轻微扩展或收缩，提升识别机会

    for idx, box in enumerate(boxes_sorted):
        x1, y1, x2, y2 = map(int, box)
        found_char = None
        found_cxy = None

        for resize_wh in resize_options:
            for pad in pad_options:
                # 计算修正后的裁剪框（限制在图片范围内）
                lx = max(0, x1 + pad)
                ty = max(0, y1 + pad)
                rx = min(img_w, x2 - pad) if (x2 - pad) > 0 else x2
                by = min(img_h, y2 - pad) if (y2 - pad) > 0 else y2
                if rx - lx <= 0 or by - ty <= 0:
                    continue
                cropped = img.crop((lx, ty, rx, by)).resize(resize_wh)
                bio = BytesIO()
                cropped.save(bio, format="PNG")
                crop_bytes = bio.getvalue()
                try:
                    char = ocr_cls.classification(crop_bytes).strip()
                except Exception:
                    char = ""
                # 打印调试信息（可注释）
                # print(f"框 {idx} 尝试 resize={resize_wh} pad={pad} -> '{char}'")
                if len(char) == 1 and char in valid_text and char not in char_positions:
                    cx = int((x1 + x2) / 2)
                    cy = int((y1 + y2) / 2)
                    found_char = char
                    found_cxy = [cx, cy]
                    break
            if found_char:
                break

        if found_char:
            char_positions[found_char] = found_cxy
            print(f"✅ 框 {idx} 识别成功: '{found_char}' -> {found_cxy}")
        else:
            # 记录失败的框便于调试
            print(f"❌ 框 {idx} 识别失败或非单字：{box}")

    # 按 valid_text 的顺序收集坐标
    coords = []
    missing = []
    for ch in valid_text:
        if ch in char_positions:
            coords.append(char_positions[ch])
        else:
            missing.append(ch)

    if missing:
        # 如果有缺失，给出清晰的错误信息并尝试更宽容的二次匹配（例如接受重复字符位置）
        # 二次策略：若某些字符未识别，可尝试把所有检测到的字符按 x 排序并按顺序取前 len(valid_text) 个
        print(f"⚠ 未识别到字符: {missing}，尝试二次降级匹配...")
        # 降级匹配：把所有识别出的 char_positions 按 x 排序并取前 N
        discovered = []
        for b in boxes_sorted:
            cx = int((b[0] + b[2]) / 2)
            cy = int((b[1] + b[3]) / 2)
            discovered.append([cx, cy])
        # 如果 discovered 数量 >= 需要数量，则取最左侧的 N 个
        need = len(valid_text)
        if len(discovered) >= need:
            coords = discovered[:need]
            print("降级匹配成功，使用检测框排序的前 N 个点。")
        else:
            raise ValueError(f"识别失败，未找到这些字符：{missing}，且候选点不足以降级匹配。")

    # 最终校验：长度应等于 len(valid_text)，并且每个坐标为两元整数组
    if len(coords) != len(valid_text):
        raise ValueError(f"最终坐标数 {len(coords)} 与提示文字长度 {len(valid_text)} 不匹配")

    print(f"最终匹配坐标: {coords}")
    return coords

# ---------- JS/Python 生成 validateCode ----------
def generate_validate_code_python(coords):
    """
    coords: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
    按前端 dealMapArr 规则：每个分量 3 位补零（zfill(3)），拼接成 24 位字符串
    """
    if not coords or not isinstance(coords, list):
        raise ValueError("coords 格式不对")
    # 取前 4 个，如果少于 4 个抛错（通常 captcha 要求4个点击）
    if len(coords) != 4:
        # 有些实现 valid_text 可能长度不是 4，可以改成按 valid_text 长度处理
        # 这里按前端 JS 需求通常是 4 个点 -> 8 个分量 -> 24 位
        raise ValueError(f"坐标个数不是 4（当前 {len(coords)}），无法生成 24 位 validateCode")
    parts = []
    for (x, y) in coords:
        xi = int(round(x))
        yi = int(round(y))
        if xi < 0 or yi < 0:
            raise ValueError("坐标包含负值")
        parts.append(f"{xi:03d}")
        parts.append(f"{yi:03d}")
    validate_code = "".join(parts)
    if len(validate_code) != 24:
        raise ValueError(f"生成的 validateCode 长度异常: {len(validate_code)}->{validate_code}")
    return validate_code

def generate_validate_code(coords):
    """
    优先尝试用本地 captcha.js（若存在且包含 dealMapArr），否则使用 Python 实现。
    coords 传入格式和前端一致，应为 [[x1,y1],...]
    """
    # 优先用本地 JS（如果可用）
    if os.path.exists(js_file):
        try:
            with open(js_file, "r", encoding="utf-8") as f:
                js_code = f.read()
            ctx = execjs.compile(js_code)
            # JS 假定 dealMapArr 接受 coords 并返回字符串
            return ctx.call("dealMapArr", coords)
        except Exception as e:
            print("调用本地 JS 生成 validateCode 失败，退回 Python 实现，错误：", e)
    # Python 备用实现
    return generate_validate_code_python(coords)

# ---------- 登录请求 ----------
def login(validate_code, encrypted_pwd):
    data = {
        "userName": username,
        "pwdEncrypt": encrypted_pwd,
        "screenDpi": screen_dpi,
        "returnUrl": return_url,
        "validateCode": validate_code
    }
    response = requests.post(login_url, headers=headers, cookies=cookies, data=data, timeout=10)
    print("登录响应:", response.text)
    return response

# ---------- 主流程 ----------
def main():
    try:
        print("开始获取验证码...")
        valid_text, image_data = get_captcha()
        print("验证码提示文字:", valid_text)

        print("开始 OCR 识别坐标...")
        coords = ocr_coords_full_recognition(image_data, valid_text)
        print("识别到坐标:", coords)

        print("生成 validateCode 参数...")
        validate_code = generate_validate_code(coords)
        print("validateCode:", validate_code)

        print("加密密码...")
        encrypted_pwd = sm2_encrypt(password, public_key, cipher_mode=0)
        print("加密后的密码:", encrypted_pwd)

        print("开始登录...")
        res = login(validate_code, encrypted_pwd)
        # 进一步根据返回做判断
        try:
            jr = res.json()
            print("返回 JSON：", jr)
        except Exception:
            print("返回文本：", res.text)

    except Exception as e:
        print("流程异常：", e)
        raise

if __name__ == "__main__":
    main()
