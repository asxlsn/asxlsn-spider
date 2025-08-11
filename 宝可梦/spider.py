import execjs
import requests


with open("code.js", "r", encoding="utf-8") as f:
    js_code = f.read()
ctx = execjs.compile(js_code)
result_params = ctx.call("get_signature")




headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Referer": "https://servicewechat.com/wx7de448cfe10bf499/133/page-frame.html",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
    "api-access-token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uSWQiOiI1RDRFNzI2MkExMUM0QUEwQjdEMzUxQTc0REMwNkU2QyIsIm9wZXJhdG9ySWQiOiIxNDA0ODExIn0.iDnwz6lTWkhLgFqrBkJFdBTsmpSCsRZ_41O1wpHwMOA",
    "nonce": str(result_params['nonce']),
    "signature": str(result_params['signature']),
    "timestamp": result_params['timestamp'],
    "xweb_xhr": "1"
}
url = "https://app-api.pokemon-tcg.cn/app-api/v1/app/customerInfo/get"
response = requests.get(url, headers=headers)
result_data = ctx.call("aesDecrypt", response.text)
print(result_data)


