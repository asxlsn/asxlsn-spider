import requests
import pandas as pd
import time
from tqdm import tqdm


def fetch_job_data(page):
    base_url = "https://www.ncss.cn/student/jobs/jobslist/ajax/"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "$Cookie": "SESSION=8371e840-30ae-4e76-b743-9ca637a13cec; XSRF-CCKTOKEN=73d9271b2fe4e626d251d301b6ddd5d5; _abfpc=2efef21a7202b3891ba4d724d6cc5c96c184dfeb_2.0; cna=1a9e2a47231636ffc1133d4c115c32f8; _gid=GA1.2.1206973841.1751176809; Hm_lvt_378ff17a1ac046691cf78376632d1ed4=1751176089,1751187223,1751195679; HMACCOUNT=29C8E5B0264CE645; aliyungf_tc=baccc5104d210ecc112c06ae1197488b8c314a011006ee9188aefbf964864842; acw_tc=ac11000117511956874248388ed12a86f1a3c00a0c506ea6a752c932d79194; CHSICC_CLIENTFLAGSTUDENT=e1b7ebb34549c59b96ad96d6d23151dd; CHSICC01=\\u00216nDWAYRxYUlwMdXzYxYLahOzddj6Y6t57HdNiGqH5MAT/HyWmMrMqTRumLe9GLfkXHIYASoJYOmI; _gat_gtag_UA_105074615_1=1; _ga_6CXWRD3K0D=GS2.1.s1751195679$o5$g1$t1751195773$j41$l0$h0; _ga=GA1.1.1188053884.1751176090; Hm_lpvt_378ff17a1ac046691cf78376632d1ed4=1751195773",
        "Pragma": "no-cache",
        "Referer": "https://job.ncss.cn/student/jobs/index.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    params = {
        "jobType": "",
        "areaCode": "510100",
        "jobName": "数据分析",
        "monthPay": "",
        "industrySectors": "",
        "property": "",
        "categoryCode": "01",
        "memberLevel": "",
        "recruitType": "",
        "offset": page,
        "limit": 10,
        "keyUnits": "",
        "degreeCode": "",
        "sourcesName": "0",
        "sourcesType": "",
        "_": int(time.time() * 1000)  # 当前时间戳
    }

    try:
        response = requests.get(base_url, headers=headers,params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("flag") and "list" in data.get("data", {}):
            return data["data"]["list"]
        return []
    except Exception as e:
        print(f"请求第{page}页时出错: {e}")
        return []


def format_salary(row):
    """格式化薪资范围"""
    if pd.isna(row['lowMonthPay']) or pd.isna(row['highMonthPay']):
        return "面议"
    return f"{row['lowMonthPay']}k-{row['highMonthPay']}k"


def main():
    all_jobs = []
    total_pages = 10  # 获取前50页数据

    print("开始获取职位数据...")
    for page in tqdm(range(1, total_pages + 1)):
        jobs = fetch_job_data(page)
        all_jobs.extend(jobs)
        time.sleep(1)  # 避免请求过于频繁

    # 转换为DataFrame
    df = pd.DataFrame(all_jobs)

    # 数据预处理
    if 'publishDate' in df.columns:
        df['publishDate'] = pd.to_datetime(df['publishDate'], unit='ms').dt.strftime('%Y-%m-%d')

    # 合并薪资范围
    df['薪资范围'] = df.apply(format_salary, axis=1)

    # 定义中文字段名映射
    column_mapping = {
        'jobName': '职位名称',
        'degreeName': '学历要求',
        'recName': '公司名称',
        'areaCodeName': '工作地点',
        'recProperty': '公司性质',
        'recScale': '公司规模',
        'recTags': '福利待遇',
        'major': '专业要求',
        'publishDate': '发布日期',
        'headCount': '招聘人数',
        '薪资范围': '薪资范围'
    }

    # 选择并重命名列
    selected_columns = [
        '职位名称', '薪资范围', '学历要求', '公司名称', '工作地点',
        '公司性质', '公司规模', '福利待遇', '专业要求', '发布日期', '招聘人数'
    ]

    df = df.rename(columns=column_mapping)[selected_columns]

    # 保存到Excel - 修正后的部分
    output_file = "全国大学生就业网职位数据.xlsx"
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='职位数据')

            # 获取工作表对象设置列宽
            worksheet = writer.sheets['职位数据']
            worksheet.column_dimensions['A'].width = 20  # 职位名称
            worksheet.column_dimensions['B'].width = 15  # 薪资范围
            worksheet.column_dimensions['C'].width = 12  # 学历要求
            worksheet.column_dimensions['D'].width = 25  # 公司名称
            worksheet.column_dimensions['E'].width = 12  # 工作地点
            worksheet.column_dimensions['F'].width = 15  # 公司性质
            worksheet.column_dimensions['G'].width = 15  # 公司规模
            worksheet.column_dimensions['H'].width = 25  # 福利待遇
            worksheet.column_dimensions['I'].width = 25  # 专业要求
            worksheet.column_dimensions['J'].width = 12  # 发布日期
            worksheet.column_dimensions['K'].width = 10  # 招聘人数
    except Exception as e:
        print(f"保存Excel文件时出错: {e}")
        # 如果openpyxl方式失败，尝试用默认方式保存
        df.to_excel(output_file, index=False)
        print(f"已使用简单方式保存到 {output_file}")

    print(f"\n数据已保存到 {output_file}，共获取 {len(df)} 条职位信息")


if __name__ == "__main__":
    main()