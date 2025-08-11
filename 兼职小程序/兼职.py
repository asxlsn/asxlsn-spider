import requests
import json
import time
import pandas as pd

headers = {
    "authority": "joblar.tongchengjiazheng.com",
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/json",
    "referer": "https://servicewechat.com/wxf986357b3b527421/3/page-frame.html",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
    "xweb_xhr": "1"
}

url = "https://joblar.tongchengjiazheng.com/api/getIndexData"

all_jobs_data = []

# 循环爬取多页数据
for i in range(1, 5):
    print(f"正在爬取第{i}页")

    params = {
        "city_id": "2368",
        "collect_id": "",
        "keyword": "",
        "pages": str(i),
        "limit": "5",
        "token": "",
        "appid": "wxf986357b3b527421"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        # 解析数据
        data = response.json()

        # 提取并处理所有兼职信息
        job_list = data.get("data", {}).get("jobList", [])
        if job_list:
            print(f"第{i}页共有{len(job_list)}个职位:")
            for index, job in enumerate(job_list):
                title = job.get("title", "无标题")
                address = job.get("address", "无地址")
                list_name = job.get("list_name", "无标签")
                detail = job.get("detail", "详情")
                wx = job.get("wx", "没有微信")

                # 打印到控制台
                print(f"  {index + 1}. {title} {address} {list_name} {detail}  {wx}")

                # 添加到数据列表
                job_data = {
                    "页码": i,
                    "职位标题": title,
                    "地址": address,
                    "标签": list_name,
                    "详情": detail,
                    "微信": wx
                }
                all_jobs_data.append(job_data)
        else:
            print(f"第{i}页没有找到职位信息")

        # 添加延迟避免请求过快
        time.sleep(1)

    except requests.RequestException as e:
        print(f"第{i}页请求失败: {e}")
    except json.JSONDecodeError as e:
        print(f"第{i}页JSON解析失败: {e}")

# 创建DataFrame并保存到Excel
if all_jobs_data:
    df = pd.DataFrame(all_jobs_data)
    excel_filename = "兼职信息_pandas.xlsx"
    df.to_excel(excel_filename, index=False, engine='openpyxl')
    print(f"数据已保存到 {excel_filename}")
else:
    print("没有获取到任何数据")
