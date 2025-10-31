import requests
import execjs

def encrypt_password(js_file_path: str, password: str) -> str:
    """用本地JS文件的toRSAcode函数加密密码"""
    ctx = execjs.compile(open(js_file_path, encoding="utf-8").read())
    return ctx.call("toRSAcode", password)

def login(login_name: str, password: str) -> dict:
    """登录接口，返回登录数据（包含token和leaguerId）"""
    encrypted_pwd = encrypt_password("code.js", password)

    login_headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Origin": "https://www.huangshan.com.cn",
        "Pragma": "no-cache",
        "Referer": "https://www.huangshan.com.cn/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

    login_url = "https://w.huangshan.com.cn/lotsapi/leaguer/api/userLeaguer/leaguerLogin"
    login_params = {
        "loginName": login_name,
        "loginPass": encrypted_pwd,
        "merchantInfoId": "730"
    }

    response = requests.get(login_url, headers=login_headers, params=login_params)
    response.raise_for_status()
    return response.json()["data"]

def get_user_info(leaguer_id: str, token: str) -> dict:
    """用登录返回的token和leaguerId获取用户信息并解析关键字段"""
    info_headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Origin": "https://www.huangshan.com.cn",
        "Pragma": "no-cache",
        "Referer": "https://www.huangshan.com.cn/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "access-token": token,
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

    info_url = "https://w.huangshan.com.cn/lotsapi/leaguer/api/userLeaguer/manage/leaguerInfo"
    info_params = {
        "merchantInfoId": "730",
        "leaguerId": leaguer_id
    }

    response = requests.get(info_url, headers=info_headers, params=info_params)
    response.raise_for_status()
    json_data = response.json()

    data = json_data.get("data", {})
    return {
        "id": data.get("id"),
        "loginName": data.get("loginName"),
        "mobile": data.get("mobile"),
        "nickName": data.get("nickName"),
        "createTime": data.get("createTime"),
        "leaguerCode": data.get("leaguerCode"),
    }



if __name__ == "__main__":
    username = "18063514542"
    pwd = "979269asx@"
    login_data = login(username, pwd)
    user_info = get_user_info(login_data["leaguerId"], login_data["token"])
    print(f"登录成功，会员ID:", user_info["leaguerCode"])
    print("用户ID:", user_info["id"])
    print("账号:", user_info["loginName"])
    print("电话:", user_info["mobile"])
    print("昵称:", user_info["nickName"])
    print("注册时间:", user_info["createTime"])

