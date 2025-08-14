import time
import json
import hashlib
import requests

# 请求头，保持不变
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

# app_key，保持不变
app_key = "34839810"


def parse_cookie_str(cookie_str: str) -> dict:
    """
    将浏览器复制的 Cookie 字符串转为 dict
    例如：
    'a=1; b=2; c=3' -> {'a': '1', 'b': '2', 'c': '3'}
    """
    cookies = {}
    for pair in cookie_str.split(";"):
        if "=" in pair:
            try:
                k, v = pair.strip().split("=", 1)
                cookies[k] = v
            except ValueError:
                # 处理可能存在的 '=' 后面没有值的情况
                continue
    return cookies


def get_sign(token, app_key, data):
    """生成请求签名"""
    timestamp = int(time.time() * 1000)
    sign_str = f"{token}&{timestamp}&{app_key}&{data}"
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    return sign, timestamp


def goofish_search_from_string(cookie_str: str, keyword: str, page_number: int = 1):
    """
    使用 Cookie 字符串、关键词和页码执行 Goofish 搜索。

    Args:
        cookie_str (str): 从浏览器复制的原始 Cookie 字符串。
        keyword (str): 搜索的关键词。
        page_number (int): 搜索结果的页码。

    Returns:
        list: 一个字典列表，每个字典包含一个搜索结果的标题和用户昵称。
              失败时返回空列表。
    """
    # 1. 解析 Cookie 字符串
    cookies = parse_cookie_str(cookie_str)

    # 2. 构建 data 对象
    data_obj = {
        "pageNumber": page_number,
        "keyword": keyword,
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

    # 3. 从解析后的 cookies 中提取 token 并生成签名
    try:
        m_h5_tk = cookies["_m_h5_tk"]
        token = m_h5_tk.split("_")[0]
        sign, t = get_sign(token, app_key, data_str)
    except KeyError:
        print("错误: Cookie 中未找到 '_m_h5_tk'。请检查你的 Cookie 是否完整。")
        return []

    # 4. 构造请求参数
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

    # 5. 构造 POST 表单数据
    post_data = {
        "data": data_str
    }

    # 6. 发送请求并处理响应
    try:
        resp = requests.post(url="https://h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.pc.search/1.0/",
                             headers=headers, cookies=cookies, params=params, data=post_data)
        resp.raise_for_status()  # 检查请求是否成功
        response_json = json.loads(resp.text)

        data_list = response_json.get("data", {}).get("resultList", [])

        results = []
        for item in data_list:
            item_data = item.get("data", {}).get("item", {})
            if item_data:
                main_content = item_data.get("main", {}).get("exContent", {})
                if main_content:
                    results.append({
                        "title": main_content.get("title"),
                        "userNickName": main_content.get("userNickName"),
                        "price":main_content.get("price")[1]['text'],
                    })
        return results

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return []
    except json.JSONDecodeError:
        print("无法解析 JSON 响应。")
        return []


# --- 调用示例 ---
if __name__ == "__main__":
    # 你的 Cookie 字符串，直接从浏览器复制粘贴即可
    my_cookie_str = "cna=ScDaINT5Bl8CAbfdndU8CCXv; t=c70f11066425a87e6324692ed8c8097f; tracknick=xy342894735481; havana_lgc2_77=eyJoaWQiOjIyMTkxMDU5NTkzODcsInNnIjoiMTI2MDhjNGUwOTljMzllNGFjMzBjOGJmMmJjMDZkNWYiLCJzaXRlIjo3NywidG9rZW4iOiIxNHAyckd6azBCSXpXZTlUMzQ3TnZBdyJ9; _hvn_lgc_=77; havana_lgc_exp=1756710367558; xlly_s=1; unb=2219105959387; cookie2=2704e0a8894f8eb43dd6bc704553d771; mtop_partitioned_detect=1; _m_h5_tk=7527ebe5e12434aaa09cceae16acbefc_1755153834314; _m_h5_tk_enc=9923c49393b358af905fd38dfb9386f4; _samesite_flag_=true; sgcookie=E100cnnA8yVt3OlgExn6Wi%2FHkt9lkaXuXp%2BL%2BafhBnsP1u%2B3QzE%2FCa0Z2wmgV6MbEfL2%2FdojnRNhs8Bxo6aSckl9U%2Be5C0SOF6R7ctbn2JIqNUhXJ9J%2FcArDFFVboYprI2op; csg=c7202b80; _tb_token_=55eef0ebf7beb; sdkSilent=1755231596415; tfstk=gvSId8wN3XcCVJ_vR3yZc-_cZ4K7QRrqFY9RnTnEeHKKwbBv_6ReY8qWw6ANYBWevQn5aTSFag6oVLBRZJAzKPWhK3x8gS5709XhJB5gX5-8eOKyFfXPRj6hK3DiQbUVW9D77_q2p3CJXFpk333JJUe6BKdtvLnpefe6ECKJe3ppXdpHd0h-2_BTCLA9w3Ldwhe6ECdJ23hl959gRBBQhsPK4XoMg9ds20ITqeOfp4o-2G9BRiWp1OWNfpTBMUBwzwId_TIFxF4ZS3XNl__RZruMATQpvKW3ActApNSWQgyrPBBNfOIB-xo2RapWk3Lse0B6xBL1AnEx1dbOLaIhOYiJKMS2PIY_e0YyXi8Ak6MunOKpe_Yc4SmH9TBcmZ-bb2KACaCfPgux0I6i24M6o096gRwsr4j7BAmbbZ-QBepMQiy_CXgkJdv6gRwsr4YpId8aCRGIr"

    search_keyword = "手机"
    page_to_search = 2
    search_results = goofish_search_from_string(my_cookie_str, search_keyword, page_to_search)

    if search_results:
        print(f"--- 搜索关键词 '{search_keyword}'，第 {page_to_search} 页的结果 ---")
        for idx, result in enumerate(search_results, 1):
            print(f"{idx}. 标题: {result['title']}")
            print(f"   用户: {result['userNickName']}")
            print(f"   价格: {result['price']}")
            print("-" * 20)
    else:
        print(f"未找到 '{search_keyword}' 的搜索结果，或请求失败。")