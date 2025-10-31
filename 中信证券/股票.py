import requests
import pandas as pd
import time
import random
from tqdm import tqdm


def crawl_stock_data(max_pages=None, delay_range=(1, 3), page_size=20):
    """
    爬取中信证券股票数据并保存到Excel文件

    参数:
    max_pages (int): 最大爬取页数，None表示爬取所有页面
    delay_range (tuple): 随机延迟范围(最小秒数, 最大秒数)
    page_size (int): 每页数据条数

    返回:
    DataFrame: 爬取到的数据
    """

    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://pb.citics.com",
        "Pragma": "no-cache",
        "Referer": "https://pb.citics.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

    url = "https://kong.citics.com/pub/api/v1/website/rzrq/punching"

    # 获取总页数
    data = {
        "pageSize": str(page_size),
        "currPage": "1"
    }
    total_pages = requests.post(url, headers=headers, data=data).json()["data"]["totalPage"]

    # 如果指定了最大页数，则取较小值
    if max_pages is not None:
        total_pages = min(total_pages, max_pages)

    # 收集所有数据
    all_info = []

    # 使用 tqdm 创建进度条
    for page in tqdm(range(1, total_pages + 1), desc="爬取进度"):
        data = {
            "pageSize": str(page_size),
            "currPage": str(page)
        }
        try:
            response = requests.post(url, headers=headers, data=data).json()["data"]["data"]

            # 将数据存储到列表中，按照指定的表头顺序
            for i in response:
                all_info.append({
                    "市场": i["exchangeCode"],
                    "证券代码": i["stockCode"],
                    "证券简称": i["stockName"],
                    "折算率": i["percent"],
                    "日期": i["dataDate"],
                    "买入及转入状态": i["status"],
                    "证券集中度分组": i["stockgroup_name"]
                })
        except Exception as e:
            print(f"爬取第{page}页时出错: {e}")
            continue

        # 添加随机延迟，防止访问过于频繁
        delay = random.uniform(delay_range[0], delay_range[1])
        time.sleep(delay)

    return all_info


def save_to_excel(data, filename="股票数据.xlsx"):
    """
    将数据保存到Excel文件

    参数:
    data (list): 股票数据列表
    filename (str): 保存的文件名
    """
    # 创建 DataFrame
    df = pd.DataFrame(data)

    # 保存到 Excel 文件
    df.to_excel(filename, index=False)

    print(f"数据保存完成，共{len(data)}条记录，已保存到{filename}")


# 使用示例
if __name__ == "__main__":
    # 爬取前5页数据
    stock_data = crawl_stock_data(max_pages=5)

    # 保存到Excel文件
    save_to_excel(stock_data)

