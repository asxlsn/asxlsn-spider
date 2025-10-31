import requests
import os
import re
import time
import openpyxl
from urllib.parse import urlsplit
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import threading

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 "
                  "NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) "
                  "WindowsWechat(0x63090c37) XWEB/14185 Flue",
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'x-requested-with': "XMLHttpRequest",
    'sec-fetch-site': "same-origin",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'accept-language': "zh-CN,zh;q=0.9",
    'priority': "u=1, i",
    'Cookie': "vipAdvert_1121292=true; vzan_base_userinfo=0D0A9065FB43F23DB5ABB241BBC8F400; "
              "vzanuserinfo1121292=C7F724C9E182F7C2E8D7877C89BC38; is_show_guanzhu_1121292=1"
}

BASE_PARAMS = {
    'id': "1121292",
    'MinisnsId': "1121292",
    'typeId': "578601",
    'h': "0",
    'hongbao': "",
    'rspan': "1",
    'wd': ""
}

URL = "https://www.weizan.cn/f/getarticlebottom"
SAVE_ROOT = "租房图片"
os.makedirs(SAVE_ROOT, exist_ok=True)

excel_lock = threading.Lock()  # 保护Excel写入和seen_ids操作的锁

def sanitize_filename(name, max_len=50):
    if not name:
        return "default_user"
    pattern = r'[^\w\s\-—()\u4e00-\u9fa5]'
    cleaned = re.sub(pattern, '_', name)
    cleaned = re.sub(r'_+', '_', cleaned)
    cleaned = cleaned.strip(" _-")
    return cleaned[:max_len] if cleaned else "default_user"

def clean_text_for_excel(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = ''.join(ch for ch in text if ch == '\t' or ch == '\n' or ch == '\r' or
                   (0x20 <= ord(ch) <= 0xD7FF) or (0xE000 <= ord(ch) <= 0xFFFD))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def download_image(img_url, folder_path, idx):
    try:
        res = requests.get(img_url, timeout=15)
        if res.status_code == 200:
            ext = os.path.splitext(urlsplit(img_url).path)[-1] or ".jpg"
            filename = f"{idx}{ext}"
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "wb") as f:
                f.write(res.content)
            return (img_url, True, file_path)
        else:
            return (img_url, False, f"HTTP {res.status_code}")
    except Exception as e:
        return (img_url, False, str(e))

def crawl_page(page_index):
    params = BASE_PARAMS.copy()
    params['pageIndex'] = str(page_index)
    try:
        resp = requests.get(URL, params=params, headers=HEADERS, timeout=15)
        data = resp.json()
        return data.get("ArtList", [])
    except Exception as e:
        print(f" 请求第{page_index}页失败: {e}")
        return []

def process_page(page_index, ws, seen_ids):
    art_list = crawl_page(page_index)
    if not art_list:
        print(f" 第{page_index}页无数据，跳过。")
        return 0

    count = 0
    for art in art_list:
        post_id = art.get("Id")
        if not post_id:
            continue
        with excel_lock:
            if post_id in seen_ids:
                continue
            seen_ids.add(post_id)

        raw_title = art.get("ContentDesc", "")
        raw_area = art.get("ArticleTypeName", "")
        raw_nickname = art.get("User", {}).get("NickName", "")

        title = clean_text_for_excel(raw_title)
        area = clean_text_for_excel(raw_area)
        nickname = clean_text_for_excel(raw_nickname)

        folder_name = sanitize_filename(nickname)
        if not folder_name:
            folder_name = "default_user"
        folder_path = os.path.join(SAVE_ROOT, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        images = art.get("Images") or []

        # 图片下载线程池
        with ThreadPoolExecutor(max_workers=5) as img_executor:
            futures = [
                img_executor.submit(download_image, img.get("filepath", ""), folder_path, idx + 1)
                for idx, img in enumerate(images) if img and img.get("filepath")
            ]
            for future in futures:
                img_url, success, info = future.result()
                if not success:
                    print(f" 图片下载失败: {img_url} 原因: {info}")

        with excel_lock:
            ws.append([post_id, title, area, nickname, folder_path])
            count += 1

    return count

def main(total_pages=20, max_workers=5):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "成都租房帖子"
    ws.append(["帖子ID", "标题", "区域", "作者昵称", "图片保存路径"])

    seen_ids = set()
    total_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_page, page, ws, seen_ids): page for page in range(1, total_pages + 1)}

        for future in tqdm(as_completed(futures), total=total_pages, desc="分页采集进度"):
            page_num = futures[future]
            try:
                count = future.result()
                total_count += count
            except Exception as e:
                print(f" 第{page_num}页处理异常: {e}")

    excel_path = "成都租房帖子采集结果.xlsx"
    wb.save(excel_path)
    print(f" 全部采集完成，采集帖子数：{total_count}，Excel已保存到：{excel_path}")

if __name__ == "__main__":
    main(total_pages=20, max_workers=5)
