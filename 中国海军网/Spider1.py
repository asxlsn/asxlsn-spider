import execjs
import requests
import json


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

    def find_activity(self):
        url = "https://www.hjbwg.com/ticketapi/api/activity/findActivity"
        data = {}
        response = self.session.post(url, headers=self.headers, cookies=self.cookies,
                                     data=json.dumps(data, separators=(',', ':')))
        try:
            return response.json()
        except Exception:
            return response.text

    def parse_login_response(self, login_res):
        if login_res.get('code') == 'S200':
            user_data = login_res.get('data', {})
            user_id = user_data.get('id')
            auth_token = user_data.get('authToken')
            phone = user_data.get('usePhone')
            print(f"登录成功！用户ID: {user_id}, 手机号: {phone}, Token: {auth_token}")
            return user_id
        else:
            print("登录失败:", login_res.get('msg'))
            return None

    def parse_activity_response(self, activity_res):
        if activity_res.get('code') == 'S200':
            activities = activity_res.get('data', [])
            print("活动列表:")
            for day_info in activities:
                date = day_info.get('date')
                open_status = day_info.get('open',{}).get('status',{})
                activity_num = day_info.get('list', []).get('activityOrderNum',{})
                activity_id = day_info.get('id',{})
                activity_title = day_info.get('title')
                print(f"  日期: {date}, 是否开放: {open_status}, 活动标题: {activity_title} 活动id：{activity_id} 数量: {activity_num}")
        else:
            print("获取活动失败:", activity_res.get('msg'))


if __name__ == "__main__":
    client = HjbwgClient(mobile="18063514542", pwd="979269asx@", js_encrypt_path="code.js")
    login_res = client.login()
    user_id = client.parse_login_response(login_res)

    if user_id:
        activity_res = client.find_activity()
        client.parse_activity_response(activity_res)
