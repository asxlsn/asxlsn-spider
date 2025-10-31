import time

from DrissionPage import ChromiumPage
import json
import pandas as pd
from DrissionPage import ChromiumPage, ChromiumOptions
# 初始化页面
# page = ChromiumPage()
co = ChromiumOptions().set_browser_path(r'F:\Google\Chrome\Application\chrome.exe')
page = ChromiumPage(co)
page.get('https://www.zhipin.com/web/geek/jobs?city=101270100')

# 输入搜索关键词
page.ele('css:.input').input('IT技术支持')

# 开始监听请求
page.listen.start('zpgeek/search/joblist.json')

# 点击搜索按钮
page.ele('css:.search-btn').click()

# 初始化职位信息列表
positions = []


# 设置抓取页数

seen_job_ids = set()
last_round_ids = set()
max_pages = 20
current_page = 0

while current_page < max_pages:
    print(f'滚动加载第 {current_page + 1} 页...')
    # 滚动到底部以触发加载
    page.scroll.to_bottom()
    time.sleep(2)  # 等待页面触发请求

    try:
        req = page.listen.wait(timeout=10)
        if not req:
            print('未捕获到请求，跳过本次循环')
            continue

        response = req.response

    except TimeoutError:
        print('等待响应超时，尝试继续')
        break

    job_data = response.body if isinstance(response.body, dict) else json.loads(response.body)

    if job_data.get('code') == 0:
        job_list = job_data.get('zpData', {}).get('jobList', [])
        if not job_list:
            print('没有新数据了')
            break

        for job in job_list:
            job_id = job.get('encryptJobId')
            if job_id in seen_job_ids:
                continue  # 去重，避免重复加载
            seen_job_ids.add(job_id)

            job_info = {
                '岗位名称': job.get('jobName', '未提供'),
                '招聘人': job.get('bossName', '未提供'),
                '招聘人职位': job.get('bossTitle', '未提供'),
                '薪资范围': job.get('salaryDesc', '未提供'),
                '职位要求': ', '.join(job.get('jobLabels', [])) if job.get('jobLabels') else '未提供',
                '福利': ', '.join(job.get('welfareList', [])) if job.get('welfareList') else '未提供',
                '城市': job.get('cityName', '未提供'),
                '公司': job.get('brandName', '未提供')
            }
            positions.append(job_info)

        current_page += 1
    else:
        print('请求失败:', job_data.get('message', '未知错误'))
        break

# 保存为 Excel（无 encoding）
df = pd.DataFrame(positions)
df.to_excel('Boss-it技术支持.xlsx', index=False)

# 打印简略信息
for pos in positions:
    print(f"{pos['岗位名称']} | {pos['招聘人']} | {pos['薪资范围']} | {pos['公司']} | {pos['福利']}")