import json
import requests
import datetime
import pandas as pd
import time
import random  # 添加random模块

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=1192030154&lang=zh_CN&timestamp=1756285740221",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

cookies = {
    "appmsglist_action_3868089839": "card",
    "RK": "RWfB8f4fRw",
    "ptcz": "c6ae746dcd68b3b2b8baa83595d1f8a186dbe4c158ee9767c0b8158297d2258b",
    "pgv_pvid": "3658154490",
    "fqm_pvqid": "f8d97391-5b29-44be-8274-a321357d5ab4",
    "poc_sid": "HJzCrmijPAdBEIIo0t10eg843CZ4ds_kFjkmhOLa",
    "rewardsn": "",
    "wxtokenkey": "777",
    "ua_id": "OpPT9fHxfcwxJkVcAAAAAPD7163lhuFYlXnBvhZC9G0=",
    "_clck": "1azoa3c|1|fyt|0",
    "wxuin": "56285099123888",
    "mm_lang": "zh_CN",
    "uuid": "adeed04b22fde2a096a2d33aea7352f6",
    "rand_info": "CAESINL1gYLKncbrgVbqC84V2jwApJZ+Y/Dr5StXeVdq1CMx",
    "slave_bizuin": "3868089839",
    "data_bizuin": "3868089839",
    "bizuin": "3868089839",
    "data_ticket": "EksUiTtfXKz0Q6sdCdJ0Yuln2WOQMLsqVrd5XMnDACTP8WZEWv5zwMqeBMwrW3Rq",
    "slave_sid": "eW04d3FESUJrUkhtYmhoT3Y4aDZJbEt0NmI4RFBycjU3ZHNtTDdicUlBU3ZibUlMdlcwNXBsSkFqWlRWNjQ3RWduMHE3TE9FdVdGblcxZjRHcGZDSnAyMzl5SVRTY09XYzVzbXljbnZWRng1TE51cGJvR0lOQ1lPTE1PS3N5aDFOakJQTEg3QjJQUm9JSWRj",
    "slave_user": "gh_87eb509b1274",
    "xid": "30dd5b6b99afde0e1dfe394be232d8c8",
    "cert": "F_GlFSKYNkfDulhGtsTXgG5lcn86kagR",
    "_clsk": "st9sv|1756285741457|25|1|mp.weixin.qq.com/weheat-agent/payload/record"
}

url = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish"

# 基础参数配置
base_params = {
    "sub": "list",
    "search_field": "null",
    "count": "5",
    "query": "",
    "fakeid": "MzkzMDM0ODA5OA==",
    "type": "101_1",
    "free_publish_type": "1",
    "sub_action": "list_ex",
    "fingerprint": "3ae9e5ffee17a610c9f764c1eb65983e",
    "token": "1192030154",
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1"
}

def fetch_page(begin_value):
    """
    获取指定begin值的页面数据

    Args:
        begin_value: begin参数值

    Returns:
        dict: 页面数据
    """
    params = base_params.copy()
    params["begin"] = str(begin_value)

    try:
        print(f"正在获取begin={begin_value}的数据...")
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误 (begin={begin_value}): {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析错误 (begin={begin_value}): {e}")
        return None

def process_articles_data(publish_list):
    """
    处理文章数据

    Args:
        publish_list: 发布列表数据

    Returns:
        list: 处理后的文章数据列表
    """
    articles_data = []

    for info in publish_list:
        publish_info = json.loads(info.get('publish_info', '{}'))
        appmsgex = publish_info.get('appmsgex', [])

        # 检查 appmsgex 是否为列表
        if isinstance(appmsgex, list):
            # 遍历列表中的每篇文章
            for index, article in enumerate(appmsgex):
                # 获取文章信息
                title = article.get('title', '无标题')
                link = article.get('link', '无链接')
                cover = article.get('cover', '无封面')
                digest = article.get('digest', '无摘要')
                author_name = article.get('author_name', '未知作者')
                create_time = article.get('create_time', '')

                # 转换时间戳为可读格式
                if create_time:
                    try:
                        readable_time = datetime.datetime.fromtimestamp(int(create_time))
                        formatted_time = readable_time.strftime('%Y-%m-%d %H:%M:%S')
                    except (ValueError, TypeError):
                        formatted_time = f"时间格式错误: {create_time}"
                else:
                    formatted_time = "未知时间"

                # 保存到数据列表
                articles_data.append({
                    '标题': title,
                    '链接': link,
                    '封面': cover,
                    '摘要': digest,
                    '作者': author_name,
                    '发布时间': formatted_time
                })
        else:
            print("appmsgex 不是列表格式")

    return articles_data

def main():
    all_articles = []
    page_count = 0
    max_pages = 10  # 最大爬取页数，可根据需要调整

    while page_count < max_pages:
        begin_value = page_count * 5  # 每页增加5
        data = fetch_page(begin_value)

        if not data:
            break

        publish_page = data.get('publish_page')
        if publish_page:
            publish_page = json.loads(publish_page)
            publish_list = publish_page.get('publish_list', [])
        else:
            print("未获取到发布列表")
            break

        # 如果没有更多数据，停止翻页
        if not publish_list:
            print("没有更多数据，停止翻页")
            break

        # 处理当前页的文章数据
        page_articles = process_articles_data(publish_list)
        all_articles.extend(page_articles)

        print(f"第 {page_count + 1} 页获取到 {len(page_articles)} 篇文章")

        # 增加页码计数
        page_count += 1

        # 添加随机延迟，避免请求过于频繁
        if page_count < max_pages:  # 最后一页不需要延迟
            # 生成1-3秒之间的随机延迟
            delay = random.uniform(1, 4)
            print(f"等待 {delay:.2f} 秒后继续...")
            time.sleep(delay)

    # 保存数据
    if all_articles:
        # 保存为Excel文件
        df = pd.DataFrame(all_articles)
        excel_filename = 'wechat_articles.xlsx'
        df.to_excel(excel_filename, index=False, engine='openpyxl')
        print(f"共获取 {len(all_articles)} 篇文章，已保存到 {excel_filename}")

        # 同时保存为JSON文件
        # json_filename = 'wechat_articles.json'
        # with open(json_filename, 'w', encoding='utf-8') as f:
        #     json.dump(all_articles, f, ensure_ascii=False, indent=2)
        # print(f"同时保存为JSON文件: {json_filename}")
    else:
        print("没有获取到文章数据")

if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"缺少依赖库: {e}")
        print("请安装依赖库: pip install pandas openpyxl")
    except Exception as e:
        print(f"发生未知错误: {e}")
