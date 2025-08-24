import pandas as pd
import requests
import json
import hashlib
import time

def get_token():
    """生成动态 token"""
    current_time = int(time.time() * 1000)
    n = "Uu0KfOB8iUP69d3c:" + str(current_time)
    token = hashlib.md5(n.encode('utf-8')).hexdigest()
    return {
        'token': token,
        'time': current_time
    }

def fetch_action_field(date="2025-08-22"):
    """
    获取韭研公社异动数据

    Args:
        date (str): 日期，格式 "YYYY-MM-DD"

    Returns:
        list: 异动数据列表（不包含第一条空数据）
    """
    token_info = get_token()

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://www.jiuyangongshe.com",
        "Referer": "https://www.jiuyangongshe.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "platform": "3",
        "timestamp": str(token_info['time']),
        "token": token_info['token']
    }

    cookies = {
        "SESSION": "MzlmNmZjMDUtMjI0ZC00ZDgwLTg3NTUtMWVhZTNhN2I2MjFk"
    }

    url = "https://app.jiuyangongshe.com/jystock-app/api/v1/action/field"
    payload = json.dumps({"date": date, "pc": 1}, separators=(',', ':'))

    try:
        response = requests.post(url, headers=headers, cookies=cookies, data=payload, timeout=10)
        response.raise_for_status()
        data = response.json().get("data", [])
        return data[1:]  # 去掉第一条空数据
    except requests.RequestException as e:
        print(f"请求异常: {e}")
        return []
    except json.JSONDecodeError:
        print("响应非 JSON 格式")
        return []


def extract_action_info(response):
    """
    提取股票名称、最新价格、涨跌幅、涨停时间，并格式化

    Args:
        response (list): fetch_action_field 返回的数据

    Returns:
        list[dict]: 每条异动对应的字典，包含
            - name: 股票名称
            - price: 最新价格（两位小数）
            - shares_range: 涨跌幅（百分比）
            - time: 涨停时间
    """
    result_list = []
    for data in response:
        plate_name = data.get('name')
        for item in data.get("list", []):
            action_info = item.get("article", {}).get("action_info", {})

            # 股票名称
            name = item.get("name", "")

            #股票代码
            code = item.get("code", "")

            # N天N版
            num = action_info.get("num", {})

            # price 转为两位小数
            price = action_info.get("price")

            if price is not None:
                price = round(price / 100, 2)  # 假设原数据是分

            # shares_range 转为百分比
            shares_range = action_info.get("shares_range")
            if shares_range is not None:
                shares_range = round(shares_range / 100, 2)  # 假设原数据是整数 * 100

            # time 保留原样
            time_str = action_info.get("time")

            result_list.append({
                "板块名称": plate_name,
                "股票代码": code,
                "股票名称": name,
                "N天N版": num,
                "最新价": price,
                "涨跌幅": shares_range,
                "涨停时间": time_str
            })
    return result_list

def count_stocks(extracted_data):
    """
    统计股票数量

    Args:
        extracted_data (list): extract_action_info 返回的数据

    Returns:
        int: 股票总数
    """
    return len(extracted_data)

def count_stocks_by_plate(extracted_data):
    """
    按板块统计股票数量

    Args:
        extracted_data (list): extract_action_info 返回的数据

    Returns:
        dict: 各板块股票数量统计
    """
    plate_count = {}
    for item in extracted_data:
        plate_name = item.get("板块名称", "未知板块")
        plate_count[plate_name] = plate_count.get(plate_name, 0) + 1
    return plate_count

def to_dataframe_full(extracted_data):
    """
    将提取的数据转换为完整 DataFrame，包括板块名称、个股名称、个股代码、
    N天N板、最新价、涨跌幅、涨停时间，并按板块分组、N天N板降序排列
    """
    df = pd.DataFrame(extracted_data)

    # 重命名列名
    df = df.rename(columns={
        "股票名称": "个股名称",
        "股票代码": "个股代码",
        "N天N版": "N天N板",
        "最新价": "最新价",
        "涨跌幅": "涨跌幅",
        "涨停时间": "涨停时间"
    })

    # 按板块名称分组，组内按 N天N板 降序排序
    df = df.sort_values(by=["板块名称", "N天N板"], ascending=[True, False]).reset_index(drop=True)

    return df


if __name__ == "__main__":
    # 获取并提取数据
    raw_data = fetch_action_field("2025-08-22")
    extracted_data = extract_action_info(raw_data)

    # 转为完整 DataFrame
    df_full = to_dataframe_full(extracted_data)

    # 打印表格
    print(df_full)

    # 写入 Excel 文件
    excel_file = "stocks_action_full.xlsx"
    df_full.to_excel(excel_file, index=False)
    print(f"数据已写入 {excel_file}")

