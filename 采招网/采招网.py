import json
import logging
import os
import requests
import execjs
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def load_js_decrypt_function(js_file_path="采招网.js"):
    """加载JavaScript解密函数"""
    try:
        with open(js_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            js_code = f.read()
        return execjs.compile(js_code)
    except Exception as e:
        logger.error(f"加载JS解密函数失败: {e}")
        return None


def fetch_data(page, keywords="%e8%b6%85%e5%a3%b0%e5%88%80"):
    """从API获取数据并解密"""
    headers = {
        "accept": "text/plain, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://search.bidcenter.com.cn",
        "pragma": "no-cache",
        "referer": "https://search.bidcenter.com.cn/",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
    }

    url = "https://interface.bidcenter.com.cn/search/GetSearchProHandler.ashx"
    data = {
        "from": "6137",
        "guid": "5142a37c-ae31-4ec3-b879-9920e7c08a7b",
        "location": "6138",
        "token": "",
        "keywords": keywords,
        "mod": "0",
        "page": str(page)
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"请求失败 (页面 {page}): {e}")
        return None


def process_results(decrypted_data, output_file=None):
    """处理并保存解密后的数据"""
    if not decrypted_data or "other2" not in decrypted_data or "listData" not in decrypted_data["other2"]:
        logger.warning("解密数据格式无效")
        return []

    results = []
    for item in decrypted_data["other2"]["listData"]:
        result = {
            "type_des": item.get("news_type_des", ""),
            "title": item.get("news_title_show", ""),
            "time": item.get("news_star_time_show", ""),
            "attachment": item.get("contain_kwd_fujian", ""),
            "location": item.get("news_diqustr", ""),
            "amount": item.get("news_zhongbiaojine_show", "")
        }
        results.append(result)

        # 打印结果
        print(
            result["type_des"],
            result["title"],
            result["time"],
            result["attachment"],
            result["location"],
            result["amount"]
        )

    # 如果提供了输出文件，保存结果
    if output_file and results:
        try:
            with open(output_file, 'a', encoding='utf-8') as f:
                for result in results:
                    f.write(json.dumps(result, ensure_ascii=False) + '\n')
        except Exception as e:
            logger.error(f"保存结果失败: {e}")

    return results


def main(start_page=1, end_page=5, keywords="%e8%b6%85%e5%a3%b0%e5%88%80", save_results=True):
    """主函数"""
    # 创建输出目录
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # 创建输出文件
    output_file = None
    if save_results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"采招网数据_{timestamp}.json")

    # 加载JavaScript解密函数
    js_ctx = load_js_decrypt_function()
    if not js_ctx:
        logger.error("无法加载JS解密函数，程序终止")
        return

    # 爬取数据
    all_results = []
    for page in range(start_page, end_page + 1):
        logger.info(f"正在爬取第 {page} 页")
        encrypted_data = fetch_data(page, keywords)

        if not encrypted_data:
            logger.warning(f"无法获取第 {page} 页数据，跳过")
            continue

        try:
            decrypted_data = js_ctx.call('AESDecrypt', encrypted_data)
            page_results = process_results(decrypted_data, output_file)
            all_results.extend(page_results)
        except Exception as e:
            logger.error(f"处理第 {page} 页数据失败: {e}")

    logger.info(f"爬取完成，共获取 {len(all_results)} 条数据")
    if save_results and all_results:
        logger.info(f"结果已保存至 {output_file}")

    return all_results


if __name__ == "__main__":
    main()


