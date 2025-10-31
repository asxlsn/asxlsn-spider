import requests
import json

headers = {
    "authority": "rf.rufengart.com",
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "referer": "https://servicewechat.com/wxea90b134044dcabc/11/page-frame.html",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
    "xweb_xhr": "1"
}

url = "https://rf.rufengart.com/app/index.php"
params = {
    "i": "2",
    "t": "0",
    "v": "2.1",
    "from": "wxapp",
    "c": "entry",
    "a": "wxapp",
    "do": "Sequence",
    "": "",
    "sign": "2c5cf2f7d4ca865fec00e0cc4221284e"
}

data = {
    "uid": "2283",
    "op": "getallspecial",
    "m": "goouc_fullexam"
}

response = requests.post(url, headers=headers, params=params, data=data)



response_data = response.json()

print(json.dumps(response_data, indent=2, ensure_ascii=False))

