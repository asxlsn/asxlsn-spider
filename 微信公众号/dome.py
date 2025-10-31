import json
import requests
import datetime
import pandas as pd
from pprint import pprint

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

"""
需要提交的data
以下个别字段是否一定需要还未验证。
注意修改token,number
number表示从第number页开始爬取，为5的倍数，从0开始。如0、5、10……
token可以使用Chrome自带的工具进行获取
fakeid是公众号独一无二的一个id，等同于后面的__biz
"""
params = {
    "sub": "list",
    "search_field": "null",
    "begin": "5",
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

try:
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    response.raise_for_status()  # 检查HTTP错误
    data = response.json()

    publish_page = data.get('publish_page')
    if publish_page:
        publish_page = json.loads(publish_page)
        publish_list = publish_page.get('publish_list', [])
    else:
        print("未获取到发布列表")
        publish_list = []

    articles_data = []  # 用于存储所有文章数据

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

                # 打印文章信息
                print(f"标题: {title}")
                print(f"链接: {link}")
                print(f"封面: {cover}")
                print(f"摘要: {digest}")
                print(f"作者: {author_name}")
                print(f"发布时间: {formatted_time}")
                print("-" * 50)

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

    # 保存为Excel文件
    if articles_data:
        df = pd.DataFrame(articles_data)
        # 保存为Excel文件
        excel_filename = 'wechat_articles.xlsx'
        df.to_excel(excel_filename, index=False, engine='openpyxl')
        print(f"共获取 {len(articles_data)} 篇文章，已保存到 {excel_filename}")

        # 同时保存为JSON文件（可选）
        json_filename = 'wechat_articles.json'
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(articles_data, f, ensure_ascii=False, indent=2)
        print(f"同时保存为JSON文件: {json_filename}")
    else:
        print("没有获取到文章数据")

except requests.exceptions.RequestException as e:
    print(f"网络请求错误: {e}")
except json.JSONDecodeError as e:
    print(f"JSON解析错误: {e}")
except ImportError as e:
    print(f"缺少依赖库: {e}")
    print("请安装依赖库: pip install pandas openpyxl")
except Exception as e:
    print(f"发生未知错误: {e}")
