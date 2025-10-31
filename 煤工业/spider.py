import time
from pprint import pprint
import requests
import json
import pandas as pd
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "https://webhr.shccig.com",
    "Pragma": "no-cache",
    "Referer": "https://webhr.shccig.com/webhrN2-zp/zwlist/NzpType-2/%E6%A0%A1%E5%9B%AD%E6%8B%9B%E8%81%98",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "webhrtoken": "43076e59-dfad-4f0a-bed6-84acbbd669a4"
}
cookies = {
    "JSESSIONID": "424A47007D068D9B3E8801986350E88D",
    "token": "43076e59-dfad-4f0a-bed6-84acbbd669a4"
}
url = "https://webhr.shccig.com/webhr/NzpPortalFirst/getNzpUnitJobData"

# 存储所有职位信息的列表
all_jobs = []

for i in range(1, 6):
    data = {
        "nzp_unit_key": "[\"1\"]",
        "conditions": "[\"\",\"\"]",
        "page": i,
        "rows": 20,
        "records": 530,
        "searchText": "",
        "nzp_type": "NzpType-2",
        "nzp_adress": "[]",
        "signature": "veQffoRjFA8In+jXtUsMi1JcHUwogiYeolLSJsP0i8jzRVL46TgT0cNvzWI4Hf1CMVpERCQoqbCyE4D9s97jxg==",
        "timestamp": "1760254224690"
    }

    try:
        response = requests.post(url, headers=headers, cookies=cookies, data=json.dumps(data, separators=(',', ':')))
        response.raise_for_status()  # 检查HTTP错误

        response_json = response.json()
        if response_json.get("data") and response_json["data"].get("data") and response_json["data"]["data"].get(
                "data"):
            job_list = response_json["data"]["data"]["data"]
            logger.info(f"第{i}页数据获取成功，共{len(job_list)}条记录")

            # 提取详细信息
            for job_key, job_info in job_list.items():
                job_detail = {
                    "职位名称": job_info.get('nzp_job_name', ''),
                    "公司名称": job_info.get('unit_name', ''),
                    "工作地点": job_info.get('nzp_address', ''),
                    "招聘人数": job_info.get('nzp_num', 0),
                    "学历要求": job_info.get('edu_demand', ''),
                    "专业要求": job_info.get('major_demand', ''),
                    "薪资待遇": job_info.get('nzp_salary', ''),
                    "发布日期": job_info.get('pub_date', ''),
                    "招聘状态": job_info.get('nzp_state', ''),
                    "职位ID": job_info.get('nzp_planjob_key', ''),
                    "单位ID": job_info.get('nzp_unit_key', '')
                }
                all_jobs.append(job_detail)

                # 使用logger打印岗位详细信息
                logger.info(f"岗位信息 - 职位名称: {job_detail['职位名称']}, "
                           f"公司名称: {job_detail['公司名称']}, "
                           f"工作地点: {job_detail['工作地点']}, "
                           f"招聘人数: {job_detail['招聘人数']}, "
                           f"学历要求: {job_detail['学历要求']}, "
                           f"专业要求: {job_detail['专业要求']}, "
                           f"薪资待遇: {job_detail['薪资待遇']}, "
                           f"发布日期: {job_detail['发布日期']}, "
                           f"招聘状态: {job_detail['招聘状态']}")
        else:
            logger.warning(f"第{i}页没有找到预期的数据结构")

    except requests.exceptions.RequestException as e:
        logger.error(f"请求第{i}页时发生网络错误: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"解析第{i}页JSON时出错: {e}")
    except KeyError as e:
        logger.error(f"第{i}页返回数据缺少必要字段: {e}")

    # 添加延时避免频繁请求
    time.sleep(1)

# 将数据写入Excel文件
if all_jobs:
    df = pd.DataFrame(all_jobs)
    df.to_excel("煤工业招聘信息.xlsx", index=False, engine='openpyxl')
    logger.info(f"数据已保存到Excel文件，共{len(all_jobs)}条记录")
else:
    logger.warning("未获取到任何数据，Excel文件未生成")
