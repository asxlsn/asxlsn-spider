import customtkinter as ctk
import threading
import time
import execjs
import requests
import json
from datetime import datetime


class HjbwgClient:
    def __init__(self, mobile, pwd):
        self.session = requests.Session()
        self.mobile = mobile
        self.pwd = pwd
        self.auth_token = None
        self.js_path = "code.js"  # JS 文件路径写死
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://www.hjbwg.com",
            "Referer": "https://www.hjbwg.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }
        with open(self.js_path, encoding="utf-8") as f:
            self.js_ctx = execjs.compile(f.read())

    def log(self, msg):
        app.log_message(msg)

    def set_auth_token(self, token):
        self.auth_token = token
        self.headers['authToken'] = token
        self.session.cookies.set('authToken', token)

    def encrypt_password(self):
        return self.js_ctx.call("encryptBy3DES", self.pwd)

    def login(self):
        url = "https://www.hjbwg.com/blueapi/api/user/userLogin"
        data = {
            "mobile": self.mobile,
            "pwd": self.encrypt_password()
        }
        try:
            res = self.session.post(url, headers=self.headers, data=json.dumps(data))
            res_json = res.json()
            if res_json.get("code") == "S200":
                token = res_json["data"].get("authToken")
                self.set_auth_token(token)
                self.log(f"登录成功！用户ID: {res_json['data'].get('id')} 手机: {res_json['data'].get('usePhone')}")
                return True
            else:
                self.log(f"登录失败: {res_json.get('msg')}")
                return False
        except Exception as e:
            self.log(f"登录异常: {e}")
            return False

    def find_activity(self):
        url = "https://www.hjbwg.com/ticketapi/api/activity/findActivity"
        try:
            res = self.session.post(url, headers=self.headers, data=json.dumps({}))
            res_json = res.json()
            if res_json.get("code") == "S200":
                activities = res_json.get("data", [])
                if not activities:
                    self.log("暂无活动数据")
                else:
                    for day_info in activities:
                        date = day_info.get('date')
                        open_status = "开放" if day_info.get('open') else "未开放"
                        event_count = len(day_info.get('list', []))
                        self.log(f"日期: {date} | 状态: {open_status} | 活动数: {event_count}")
            else:
                self.log(f"获取活动失败: {res_json.get('msg')}")
        except Exception as e:
            self.log(f"活动查询异常: {e}")


class TicketApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("自动检测门票工具")
        self.geometry("650x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # 变量
        self.running = False
        self.client = None

        # 登录信息 Frame
        login_frame = ctk.CTkFrame(self)
        login_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(login_frame, text="手机号:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_mobile = ctk.CTkEntry(login_frame, width=200)
        self.entry_mobile.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(login_frame, text="密码:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_pwd = ctk.CTkEntry(login_frame, width=200, show="*")
        self.entry_pwd.grid(row=0, column=3, padx=5, pady=5)

        # 设置 Frame
        setting_frame = ctk.CTkFrame(self)
        setting_frame.pack(padx=10, pady=5, fill="x")

        ctk.CTkLabel(setting_frame, text="检测间隔(分钟):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_interval = ctk.CTkEntry(setting_frame, width=100)
        self.entry_interval.insert(0, "1")
        self.entry_interval.grid(row=0, column=1, padx=5, pady=5)

        self.btn_start = ctk.CTkButton(setting_frame, text="开始检测", command=self.start_check)
        self.btn_start.grid(row=0, column=2, padx=10, pady=5)

        self.btn_stop = ctk.CTkButton(setting_frame, text="停止检测", command=self.stop_check)
        self.btn_stop.grid(row=0, column=3, padx=10, pady=5)

        # 日志 Frame
        log_frame = ctk.CTkFrame(self)
        log_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.text_log = ctk.CTkTextbox(log_frame, wrap="word")
        self.text_log.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(log_frame, command=self.text_log.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_log.configure(yscrollcommand=scrollbar.set)

    def log_message(self, msg):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        self.text_log.insert("end", f"{timestamp} {msg}\n")
        self.text_log.see("end")

    def start_check(self):
        if self.running:
            self.log_message("检测已在运行中...")
            return

        mobile = self.entry_mobile.get().strip()
        pwd = self.entry_pwd.get().strip()
        interval = self.entry_interval.get().strip()

        if not mobile or not pwd or not interval.isdigit():
            self.log_message("请输入有效的手机号、密码和检测间隔")
            return

        self.client = HjbwgClient(mobile, pwd)
        if not self.client.login():
            return

        self.running = True
        self.log_message("开始自动检测活动...")
        threading.Thread(target=self.check_loop, args=(int(interval),), daemon=True).start()

    def stop_check(self):
        self.running = False
        self.log_message("已停止检测")

    def check_loop(self, interval):
        while self.running:
            self.client.find_activity()
            time.sleep(interval * 60)


if __name__ == "__main__":
    app = TicketApp()
    app.mainloop()
