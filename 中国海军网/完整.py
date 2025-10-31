import requests
import execjs
import json
import base64
import ddddocr


class HjbwgClient:
    def __init__(self, mobile, pwd, js_encrypt_path, auth_token=None):
        self.session = requests.Session()
        self.mobile = mobile
        self.pwd = pwd
        self.auth_token = auth_token
        self.headers = {
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
            "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        self.cookies = {}
        if auth_token:
            self.set_auth_token(auth_token)

        with open(js_encrypt_path, encoding="utf-8") as f:
            self.js_ctx = execjs.compile(f.read())

    def set_auth_token(self, auth_token):
        self.auth_token = auth_token
        self.cookies['authToken'] = auth_token
        self.headers['authToken'] = auth_token

    def encrypt_password(self):
        return self.js_ctx.call("encryptBy3DES", self.pwd)

    def login(self):
        """登录并保存 token"""
        url = "https://www.hjbwg.com/blueapi/api/user/userLogin"
        pwd_encrypted = self.encrypt_password()
        data = {
            "mobile": self.mobile,
            "pwd": pwd_encrypted
        }
        response = self.session.post(url, headers=self.headers, cookies=self.cookies,
                                     data=json.dumps(data, separators=(',', ':')))
        try:
            res_json = response.json()
            if res_json.get("code") == "S200" and "data" in res_json:
                new_token = res_json["data"].get("authToken")
                if new_token:
                    self.set_auth_token(new_token)
            return res_json
        except Exception:
            return response.text

    def get_activity_detail(self, activity_id):
        """获取单个活动的可预约时间段信息"""
        url = "https://www.hjbwg.com/ticketapi/api/activity/getActivityTimeNum"
        data = {"activityId": activity_id}
        response = self.session.post(url, headers=self.headers, cookies=self.cookies,
                                     data=json.dumps(data, separators=(',', ':')))
        try:
            print("获取活动详情:", response.json())
            return response.json()
        except Exception:
            return response.text

    def get_first_available_slot(self, activity_id):
        """获取第一个可预约的时间段"""
        detail_res = self.get_activity_detail(activity_id)
        if not isinstance(detail_res, dict) or detail_res.get("code") != "S200":
            print("获取活动详情失败:", detail_res)
            return None, None

        for slot in detail_res.get("data", []):
            if slot.get("status") == "YES" and slot.get("activityNum", 0) > 0:
                date = slot.get("activityVisitDate")
                time_slot = slot.get("timeInterval")
                print(f"找到可预约时间段: {date} {time_slot}")
                return date, time_slot

        print("没有找到可预约的时间段")
        return None, None

    def get_validate_code(self):
        """获取验证码并用 ddddocr 识别"""
        url = "https://www.hjbwg.com/blueapi/api/user/ck/getImageValidateCode"
        response = self.session.post(url, headers=self.headers, cookies=self.cookies,
                                     data=json.dumps({}, separators=(',', ':')))
        try:
            res_json = response.json()
            base64_str = res_json.get("data", "")
            if not base64_str:
                print("验证码获取失败:", res_json)
                return None

            img_bytes = base64.b64decode(base64_str)
            # 这里保存验证码图片方便调试
            with open("captcha.jpg", "wb") as f:
                f.write(img_bytes)

            ocr = ddddocr.DdddOcr()
            code = ocr.classification(img_bytes)
            print(f"验证码识别结果: {code}")
            return code
        except Exception as e:
            print("验证码解析失败:", e)
            return None

    def create_order(self, activity_id, date, time_slot, liaison_name, liaison_phone, id_card, validate_code):
        """提交预约订单"""
        url = "https://www.hjbwg.com/ticketapi/api/activityOrder/ck/addActivityOrder"
        data = {
            "activityOrder": {
                "activityId": activity_id,
                "liaisonPhone": liaison_phone,
                "liaisonUser": liaison_name,
                "activityVisitDate": date,
                "activityVisitTime": time_slot
            },
            "activityMemberList": [
                {
                    "userName": liaison_name,
                    "userIdCard": id_card,
                    "userPhone": "",
                    "userCertificateType": "ID_CARD",
                    "ticketType": "VISIT_TICKET"
                }
            ],
            "validateCode": validate_code
        }
        response = self.session.post(url, headers=self.headers, cookies=self.cookies,
                                     data=json.dumps(data, separators=(',', ':')))
        try:
            return response.json()
        except Exception:
            return response.text

    def run(self, activity_id, liaison_name, liaison_phone, id_card):
        print("正在登录...")
        login_res = self.login()
        if not isinstance(login_res, dict) or login_res.get("code") != "S200":
            print("登录失败:", login_res)
            return

        print("登录成功，正在获取活动时间段...")
        date, time_slot = self.get_first_available_slot(activity_id)
        if not date or not time_slot:
            print("没有可预约时间段，退出")
            return

        print("正在获取并识别验证码...")
        validate_code = self.get_validate_code()
        if not validate_code:
            print("验证码识别失败，无法下单")
            return

        print("正在提交订单...")
        order_res = self.create_order(activity_id, date, time_slot, liaison_name, liaison_phone, id_card, validate_code)
        print("下单结果：", order_res)


if __name__ == "__main__":
    client = HjbwgClient(
        mobile="18063514542",       # 手机号
        pwd="979269asx@",               # 登录密码
        js_encrypt_path="code.js"  # 3DES加密的JS文件路径
    )
    client.run(
        activity_id=8298,
        liaison_name="杨淮琳",
        liaison_phone="18030514542",
        id_card="513721200004050179"
    )
