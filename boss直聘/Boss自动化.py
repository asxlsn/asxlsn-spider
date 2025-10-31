import time
import json
import pandas as pd
from DrissionPage import ChromiumPage, ChromiumOptions


def crawl_boss_jobs(keyword='统计', city_code='101270100', max_pages=20, output_file='职位信息.xlsx'):


    co = ChromiumOptions().set_browser_path(r'F:\Google\Chrome\Application\chrome.exe')
    page = ChromiumPage(co)
    page.get(f'https://www.zhipin.com/web/geek/jobs?city={city_code}')
    page.ele('css:.input').input(keyword)
    page.listen.start('zpgeek/search/joblist.json')
    page.ele('css:.search-btn').click()

    positions = []  # 保存所有职位数据
    seen_job_ids = set()  # 记录抓过的职位 ID，防止重复
    last_round_ids = set()  # 记录上一轮职位 ID 用于判断是否到底
    current_page = 0  # 当前页数
    no_request_count = 0  # 连续未监听到请求次数
    MAX_NO_REQ = 3  # 最大未请求次数（终止标志）

    while current_page < max_pages:
        print(f'滚动加载第 {current_page + 1} 页...')
        page.scroll.to_bottom()
        time.sleep(2)

        req = page.listen.wait(timeout=10)
        if not req:
            print('未捕获到请求，跳过本次循环')
            no_request_count += 1
            if no_request_count >= MAX_NO_REQ:
                print('连续多次未捕获到请求，认为已加载完毕，终止。')
                break
            continue
        no_request_count = 0  # ✅ 重置计数

        response = req.response
        job_data = response.body if isinstance(response.body, dict) else json.loads(response.body)

        if job_data.get('code') != 0:
            print('请求失败:', job_data.get('message', '未知错误'))
            break

        job_list = job_data.get('zpData', {}).get('jobList', [])
        if not job_list:
            print('无职位数据，结束抓取')
            break

        current_ids = set(job.get('encryptJobId') for job in job_list)
        if current_ids == last_round_ids:
            print('检测到数据无变化，终止循环')
            break
        last_round_ids = current_ids

        for job in job_list:
            job_id = job.get('encryptJobId')
            if job_id in seen_job_ids:
                continue
            seen_job_ids.add(job_id)

            job_info = {
                '岗位名称': job.get('jobName', '未提供'),
                '招聘人': job.get('bossName', '未提供'),
                '招聘人职位': job.get('bossTitle', '未提供'),
                '薪资范围': job.get('salaryDesc', '未提供'),
                '学历要求': ', '.join(job.get('jobLabels', [])) if job.get('jobLabels') else '未提供',
                '职位要求': job.get('postDescription', []),
                '福利': ', '.join(job.get('welfareList', [])) if job.get('welfareList') else '未提供',
                '城市': job.get('cityName', '未提供'),
                '公司': job.get('brandName', '未提供'),
                '公司规模': job.get('brandScaleName', '未提供'),
                '大概地址': job.get('businessDistrict', '未提供'),

            }
            positions.append(job_info)

        current_page += 1

    # 保存
    df = pd.DataFrame(positions)
    df.to_excel(output_file, index=False)
    print(f"\n共抓取 {len(positions)} 条职位信息，已保存为 {output_file}\n")

    for pos in positions[:10]:
        print(f"{pos['岗位名称']} | {pos['招聘人']} | {pos['薪资范围']} | {pos['公司']} | {pos['福利']} | {pos['公司规模']} | {pos['大概地址']}")


# 主程序入口
if __name__ == '__main__':
    crawl_boss_jobs(
        keyword='统计',
        city_code='101270100',  # 成都
        max_pages=30,
        output_file='Boss直聘-统计职位.xlsx'
    )
