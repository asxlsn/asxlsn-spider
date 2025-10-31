#api/v4/questions/1915798191015723414/feeds
import time
import json
import pandas as pd
from DrissionPage import ChromiumPage, ChromiumOptions
def crawl_boss_jobs(max_pages=20, output_file='职位信息.xlsx'):


    co = ChromiumOptions().set_browser_path(r'F:\Google\Chrome\Application\chrome.exe')
    page = ChromiumPage(co)
    page.get(f'https://www.zhihu.com/question/1915798191015723414')
    page.listen.start('api/v4/questions/1915798191015723414/feeds')
    req = page.listen.wait(timeout=10)

    response = req.response
    data = response.body if isinstance(response.body, dict) else json.loads(response.body)




# 主程序入口
if __name__ == '__main__':
    crawl_boss_jobs(
        max_pages=1,
        output_file='话题.xlsx'
    )