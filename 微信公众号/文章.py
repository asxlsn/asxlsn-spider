import json
from pprint import pprint

import requests


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
response = requests.get(url, headers=headers, cookies=cookies, params=params).json()
publish_page = response.get('publish_page')
publish_page = json.loads(publish_page)

publish_list = publish_page.get('publish_list')
# print(publish_list)

for info in publish_list:
    publish_info = json.loads(info.get('publish_info'))
    appmsgex = publish_info.get('appmsgex',{})
    print(appmsgex)

