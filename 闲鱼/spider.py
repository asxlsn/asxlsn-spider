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
    my_cookie_str = "cna=ScDaINT5Bl8CAbfdndU8CCXv; t=c70f11066425a87e6324692ed8c8097f; tracknick=xy342894735481; cookie2=162bd6e37ff63eae6f232dc67c51e017; mtop_partitioned_detect=1; _m_h5_tk=f13e1a35724844e4bd70cdcd4451d8f2_1758614181736; _m_h5_tk_enc=0896af87141e4e8eeccc581218029a3f; xlly_s=1; _samesite_flag_=true; _tb_token_=f41beae76eb3f; sgcookie=E100uXoVVl63LzRuYYHx99dSVf9KSRdyP%2FlZpPic2yA7ah3XcFMe%2BqCUulritPjhXVFZ6qNahzvjzilEklyWNrTGmaJb64aDySG4aaAp%2FojVSTiL%2BVkBwFtQXr5HqNLlale4; csg=0b05b51e; unb=2219105959387; havana_lgc2_77=eyJoaWQiOjIyMTkxMDU5NTkzODcsInNnIjoiNTQ0ZjZmMzc4NDcyMDczMzMxMTk0MGMyZTEwNDBjYTUiLCJzaXRlIjo3NywidG9rZW4iOiIxZHg3M3pvcXZfbWNpUGtzYk5vdW5fZyJ9; _hvn_lgc_=77; havana_lgc_exp=1761196844379; sdkSilent=1758691246647; tfstk=gO-KQlgMofch41PUpQ0iqus2MRMM2VvUKBJbq_f3PCd9hKPhPHjHwzdHUQbSTMxJ6M-M-ufnTgpWighmimmDLpSNVjcckXKtYi6zOTNlRG61qTEBPE1DLpSzQRVSoF9UezCgdTsWNG_1UtS7N66SBG6cUgZCPka_11W5Vg_CON91FTC7OgaIBd1NFg1WNwMOf1W5V_O5VbPYp_2CwuLCdOpsWk9QVutOpNgMd1OHTYXhJs9C6jGXXu_dGp1TVX_gTU5R_nGiWdR2RBXwwmhO4C8WNTd_1bbeFFdOpBcYa_xeK3Bwp2GpLG5pFaIYFD9Ov6QXxNwLAI99FEb9jxiVvM1BrMJuHXv9vBveXL275MIHWZKdcmPCZFvv2TKracdv3hROCIi-OgzymnQAPSfAEyMtBzzPRORjMdusc9kMGOCmIP4zzNXNBsDtBzzPROWOiAm0zz7GQ"

    search_keyword = "小米13"
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