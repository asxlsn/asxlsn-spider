import execjs
import requests

class PokemonApiClient:
    def __init__(self, js_path, api_token):
        with open(js_path, "r", encoding="utf-8") as f:
            js_code = f.read()
        self.ctx = execjs.compile(js_code)
        self.api_token = api_token
        self.base_url = "https://app-api.pokemon-tcg.cn/app-api/v1"

    def _get_signature(self):
        # 调用 JS 方法生成签名参数
        return self.ctx.call("get_signature")

    def _aes_decrypt(self, data):
        # 调用 JS 方法解密返回数据
        return self.ctx.call("aesDecrypt", data)

    def get_customer_info(self):
        sig_params = self._get_signature()
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Referer": "https://servicewechat.com/wx7de448cfe10bf499/133/page-frame.html",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 "
                          "MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows "
                          "WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
            "api-access-token": self.api_token,
            "nonce": str(sig_params['nonce']),
            "signature": str(sig_params['signature']),
            "timestamp": sig_params['timestamp'],
            "xweb_xhr": "1"
        }
        url = f"{self.base_url}/app/customerInfo/get"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        decrypted = self._aes_decrypt(response.text)
        return decrypted

# 使用示例
if __name__ == "__main__":
    api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uSWQiOiI1RDRFNzI2MkExMUM0QUEwQjdEMzUxQTc0REMwNkU2QyIsIm9wZXJhdG9ySWQiOiIxNDA0ODExIn0.iDnwz6lTWkhLgFqrBkJFdBTsmpSCsRZ_41O1wpHwMOA"
    client = PokemonApiClient(js_path="code.js", api_token=api_token)
    data = client.get_customer_info()
    print(data)
