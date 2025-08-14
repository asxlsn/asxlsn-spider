import time
import json
import hashlib
import requests

# 请求头
headers = {
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.goofish.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.goofish.com/",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

# Cookie（必须带上 _m_h5_tk 才能生成签名）
cookies = {
    "cna": "ScDaINT5Bl8CAbfdndU8CCXv",
    "t": "c70f11066425a87e6324692ed8c8097f",
    "tracknick": "xy342894735481",
    "havana_lgc2_77": "eyJoaWQiOjIyMTkxMDU5NTkzODcsInNnIjoiMTI2MDhjNGUwOTljMzllNGFjMzBjOGJmMmJjMDZkNWYiLCJzaXRlIjo3NywidG9rZW4iOiIxNHAyckd6azBCSXpXZTlUMzQ3TnZBdyJ9",
    "_hvn_lgc_": "77",
    "havana_lgc_exp": "1756710367558",
    "xlly_s": "1",
    "unb": "2219105959387",
    "cookie2": "2704e0a8894f8eb43dd6bc704553d771",
    "mtop_partitioned_detect": "1",
    "_m_h5_tk": "7527ebe5e12434aaa09cceae16acbefc_1755153834314",
    "_m_h5_tk_enc": "9923c49393b358af905fd38dfb9386f4",
    "_samesite_flag_": "true",
    "sgcookie": "E100cnnA8yVt3OlgExn6Wi%2FHkt9lkaXuXp%2BL%2BafhBnsP1u%2B3QzE%2FCa0Z2wmgV6MbEfL2%2FdojnRNhs8Bxo6aSckl9U%2Be5C0SOF6R7ctbn2JIqNUhXJ9J%2FcArDFFVboYprI2op",
    "csg": "c7202b80",
    "_tb_token_": "55eef0ebf7beb",
    "sdkSilent": "1755231596415",
    "tfstk": "gvSId8wN3XcCVJ_vR3yZc-_cZ4K7QRrqFY9RnTnEeHKKwbBv_6ReY8qWw6ANYBWevQn5aTSFag6oVLBRZJAzKPWhK3x8gS5709XhJB5gX5-8eOKyFfXPRj6hK3DiQbUVW9D77_q2p3CJXFpk333JJUe6BKdtvLnpefe6ECKJe3ppXdpHd0h-2_BTCLA9w3Ldwhe6ECdJ23hl959gRBBQhsPK4XoMg9ds20ITqeOfp4o-2G9BRiWp1OWNfpTBMUBwzwId_TIFxF4ZS3XNl__RZruMATQpvKW3ActApNSWQgyrPBBNfOIB-xo2RapWk3Lse0B6xBL1AnEx1dbOLaIhOYiJKMS2PIY_e0YyXi8Ak6MunOKpe_Yc4SmH9TBcmZ-bb2KACaCfPgux0I6i24M6o096gRwsr4j7BAmbbZ-QBepMQiy_CXgkJdv6gRwsr4YpId8aCRGIr"
}

# 生成签名函数
def get_sign(token, app_key, data):
    timestamp = int(time.time() * 1000)
    sign_str = f"{token}&{timestamp}&{app_key}&{data}"
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    return sign, timestamp

# 请求参数
url = "https://h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.pc.search/1.0/"
app_key = "34839810"

# 这里要保证和 JS 完全一致的 JSON 格式（无多余空格）
data_obj = {
    "pageNumber": 1,
    "keyword": "ipad",
    "fromFilter": False,
    "rowsPerPage": 30,
    "sortValue": "",
    "sortField": "",
    "customDistance": "",
    "gps": "",
    "propValueStr": {},
    "customGps": "",
    "searchReqFromPage": "pcSearch",
    "extraFilterValue": "{}",
    "userPositionJson": "{}"
}
data_str = json.dumps(data_obj, separators=(',', ':'))


# 从 cookie 中取 token
token = cookies["_m_h5_tk"].split("_")[0]
sign, t = get_sign(token, app_key, data_str)

# query string 参数
params = {
    "jsv": "2.7.2",
    "appKey": app_key,
    "t": str(t),
    "sign": sign,
    "v": "1.0",
    "type": "originaljson",
    "accountSite": "xianyu",
    "dataType": "json",
    "timeout": "20000",
    "api": "mtop.taobao.idlemtopsearch.pc.search",
    "sessionOption": "AutoLoginOnly",
    "spm_cnt": "a21ybx.search.0.0",
    "spm_pre": "a21ybx.search.searchInput.0"
}

# POST 表单数据
post_data = {
    "data": data_str
}


resp = requests.post(url, headers=headers, cookies=cookies, params=params, data=post_data)
print(resp.text)
print("----------------------------------------------------------------------------------------------------------------")
response = json.loads(resp.text)
data_list = response.get("data", {}).get("resultList", {})
for item in data_list:
    print(item.get("data", {}).get("item", {}).get("main", {}).get("exContent", {}).get("title"))
    print(item.get("data", {}).get("item", {}).get("main", {}).get("exContent", {}).get("userNickName"))

