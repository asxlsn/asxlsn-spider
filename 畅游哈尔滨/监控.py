import requests
import json
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime


class Bus365App:
    def __init__(self):
        # 主题设置
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")

        # 主窗口
        self.app = ctk.CTk()
        self.app.title("畅玩哈尔滨")
        self.app.geometry("520x400")
        self.app.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # 标题
        title_label = ctk.CTkLabel(self.app, text="用户界面", font=("微软雅黑", 20, "bold"))
        title_label.pack(pady=10)

        # Token输入框
        token_frame = ctk.CTkFrame(self.app, corner_radius=10)
        token_frame.pack(pady=10, padx=20, fill="x")

        token_label = ctk.CTkLabel(token_frame, text="Client Token：", font=("微软雅黑", 13))
        token_label.pack(side="left", padx=10, pady=10)

        self.token_entry = ctk.CTkEntry(token_frame, width=300, font=("微软雅黑", 12))
        self.token_entry.pack(side="right", padx=10, pady=10)

        # 按钮区
        btn_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        btn_frame.pack(pady=5)

        login_btn = ctk.CTkButton(btn_frame, text="登录", command=self.login, width=120, height=35)
        login_btn.grid(row=0, column=0, padx=10)

        clear_log_btn = ctk.CTkButton(btn_frame, text="清空日志", command=self.clear_log, width=120, height=35)
        clear_log_btn.grid(row=0, column=1, padx=10)

        # 用户信息显示
        self.nickname_label = ctk.CTkLabel(self.app, text="昵称：", font=("微软雅黑", 14))
        self.nickname_label.pack(pady=5)

        # 日志输出区
        log_label = ctk.CTkLabel(self.app, text="日志消息：", font=("微软雅黑", 13))
        log_label.pack(anchor="w", padx=20, pady=(5, 0))

        self.log_text = ctk.CTkTextbox(self.app, height=150, font=("微软雅黑", 11))
        self.log_text.pack(padx=20, pady=5, fill="both", expand=True)

    def login(self):
        clienttoken = self.token_entry.get().strip()
        if not clienttoken:
            messagebox.showwarning("提示", "请输入 Client Token！")
            return

        self.log(f"开始登录...")

        headers = {
            "Accept": "application/json, text/javascript,",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json, text/javascript",
            "Referer": "https://servicewechat.com/wx156a2bf44f571c1d/22/page-frame.html",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
            "xweb_xhr": "1"
        }

        url = "https://ftcloud.bus365.com/bus/interface/useraction/userinfo"
        params = {
            "deviceid": "1",
            "token": json.dumps({
                "clienttype": "weixx",
                "clienttoken": clienttoken,
                "ordertoken": "",
                "version": "1.3.7.6"
            }),
            "org": "88238482",
            "lang": "cn"
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()

            if data.get("status") and data.get("code") == "0000":
                nickname = data["data"].get("usernickname", "未知昵称")
                self.nickname_label.configure(text=f"昵称：{nickname}")
                self.log(f"登录成功！昵称：{nickname}")
            else:
                self.log(f"登录失败：{data.get('message', '未知错误')}")
                messagebox.showerror("错误", f"登录失败：{data.get('message', '未知错误')}")
        except Exception as e:
            self.log(f"请求异常：{e}")
            messagebox.showerror("错误", f"请求异常：{e}")

    def log(self, msg):
        """日志追加带时间"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {msg}\n")
        self.log_text.see("end")  # 自动滚动到底部

    def clear_log(self):
        """清空日志"""
        self.log_text.delete("1.0", "end")

    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    Bus365App().run()
