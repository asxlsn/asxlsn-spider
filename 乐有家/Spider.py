import json
import time

import execjs
import pandas as pd
import requests


def get_url(m):
    headers = {
        "authority": "steward.leyoujia.com",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "clientid": "oVs0Z0eheUCSdhVZI1yNeH8i3mGE",
        "clientsign": "da95f211afce4315230739469bde8cc4",
        "content-type": "application/x-www-form-urlencoded",
        "deviceid": "oVs0Z0eheUCSdhVZI1yNeH8i3mGE",
        "encrypt": "true",
        "minisystem": "miniAndroid",
        "phoneos": "miniprogram",
        "recommend": "0",
        "referer": "https://servicewechat.com/wx8d0bf76b6d106216/639/page-frame.html",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "ssid": "oVs0Z0eheUCSdhVZI1yNeH8i3mGE",
        "timestamp": "1755242766207",
        "token": "vkDMmFf4TvKUhvy247iAVw",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "userid": "8215939",
        "uuid": "on1pG1ejwdcumZ6WxvJLHGuW8cEI",
        "xweb_xhr": "1"
    }
    url = "https://steward.leyoujia.com/stewardnew/common/queryInlineCommunity"
    data = {
        # todo
        "key": m
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()
def decr_Key():
    with open("code.js", "r", encoding="utf-8") as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)
    decr_Key= ctx.call("getKey")
    return decr_Key


def decrypt_data(data):
    with open("code.js", "r", encoding="utf-8") as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)
    decrypted_str = ctx.call('aesDecrypt', data)
    print(decrypted_str)
    # 将解密后的字符串转换为JSON对象
    return json.loads(decrypted_str)

def get_detail(data):
    json_data = data.get("data", {}).get("esfs", {}).get("data", [])
    houses_data = []
    for item_list in json_data:
        houses_info = {
            "标题": item_list.get("title", ""),
            "地址": item_list.get("comAddress", ""),
            "小区": item_list.get("comName", ""),
            "面积": item_list.get("buildingArea", ""),
            "朝向": item_list.get("orientation", ""),
            "价格": item_list.get("salePrice", ""),
            "m/价格": item_list.get("saleUnitPrice", ""),
        }
        houses_data.append(houses_info)
    return houses_data


def save_to_excel(data, filename="乐有家房源信息.xlsx"):
    # 创建DataFrame
    df = pd.DataFrame(data)

    # 保存到Excel文件
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"数据已保存到 {filename}")

    return df

if __name__ == '__main__':
    decr_key = decr_Key().get("key")
    print(decr_key)
    # data = get_url(decr_key)
    # print( data)
    # json_data = decrypt_data(data)
    # print(json_data)
    # houses_data = get_detail(json_data)
    # df = save_to_excel(houses_data)







