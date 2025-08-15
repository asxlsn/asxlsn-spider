import random
import execjs
import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# === 加载 JS 加密文件 ===
with open("code.js", "r", encoding="utf-8") as f:
    js_code = f.read()
ctx = execjs.compile(js_code)

# === 请求参数配置 ===
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://www.xiniudata.com",
    "referer": "https://www.xiniudata.com/industry/newest?from=data",
    "user-agent": "Mozilla/5.0"
}
cookies = {
    "btoken": "R013OTC5U69WCXQN07AOJPKKMARY530C"
}
url = "https://www.xiniudata.com/api2/service/x_service/person_industry_list/list_industries_by_sort"

page_size = 20
total_pages = 3  # 总页数
max_workers = 3  # 并发线程数


def fetch_page(page):
    """抓取并解密单页数据"""
    start = page * page_size
    payload_data = {
        "sort": 1,
        "start": start,
        "limit": page_size
    }
    # 调用 JS 加密 + 生成 sig
    result = ctx.call("get_params", payload_data)
    f_val = result["payload"]
    sig_val = result["sig"]

    data = {
        "payload": f_val,
        "sig": sig_val,
        "v": 1
    }

    try:
        response = requests.post(url, headers=headers, cookies=cookies,
                                 data=json.dumps(data, separators=(',', ':')), timeout=10)
        resp_json = response.json()
        if "d" in resp_json:
            decrypted = ctx.call("decrypt_data", resp_json["d"])

            return page, decrypted
        else:
            return page, None
    except Exception as e:
        return page, {"error": str(e)}


if __name__ == "__main__":
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_page = {executor.submit(fetch_page, page): page for page in range(total_pages)}
        for future in as_completed(future_to_page):
            page_idx, data = future.result()
            results[page_idx] = data
            time.sleep(random.uniform(2, 5))  # 防止过快触发风控

    # 按页顺序输出
    for page in sorted(results.keys()):
        print(f"第 {page + 1} 页数据:")
        print(results[page])
