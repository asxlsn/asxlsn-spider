import os

import requests
import json


headers = {
    "Accept": "application/json",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "https://www.vcg.com",
    "Pragma": "no-cache",
    "Referer": "https://www.vcg.com/sets/580174181",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
cookies = {
    "acw_tc": "276082a717361702119936951ec3d7be63967c2e9efa1fc3cd16cc34f24f4a",
    "clientIp": "182.131.41.180",
    "uuid": "aa998563-8ae1-4be3-b2a5-b2c4507d9be1",
    "sajssdk_2015_cross_new_user": "1",
    "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%221943bcf0c1f0-057a10b72b0d8e-4c657b58-1327104-1943bcf0c2011f8%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%7D%2C%22%24device_id%22%3A%221943bcf0c1f0-057a10b72b0d8e-4c657b58-1327104-1943bcf0c2011f8%22%7D",
    "Hm_lvt_5fd2e010217c332a79f6f3c527df12e9": "1736170212",
    "HMACCOUNT": "ED27B517DF865C9C",
    "Hm_up_5fd2e010217c332a79f6f3c527df12e9": "%7B%22uuid%22%3A%7B%22value%22%3A%22aa998563-8ae1-4be3-b2a5-b2c4507d9be1%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22%22%2C%22scope%22%3A1%7D%7D",
    "fingerprint": "d5324a3db9ed470fcc0113d15a5cdaff",
    "_fp_": "eyJpcCI6IjE4Mi4xMzEuNDEuMTgwIiwiZnAiOiJkNTMyNGEzZGI5ZWQ0NzBmY2MwMTEzZDE1YTVjZGFmZiIsImhzIjoiJDJhJDA4JGMxVmowVWRxWnNpRGF4VktsVXd1Ty5iYVhhSWlnR1NhVGpXQm15LmFjM09rTjRITkd4ak9DIn0%3D",
    "ssxmod_itna": "Yq+xniDQi=G=itXK0Lx0pm1QoGkDunBplxGuRq2Kx5DsedTDSxGKidDqxBnm6rO+3oKjG2+FPV0OrAFp870O+A1Wc32atTDCPGnDB9vakDemtD5xGoDPxDeDAAqGaDb4DrnoqGp9uXvX6uDAQDQ4GyDitDKT0DxG3D0f=48Ahe8u2UGdxD0dhN5+GWDYp9jLdePWrDAMqMYGG9D0tDIqGXF09dxDUku=x/jua756puQniDtqD98mUXWn4BlqNRK6+AK0Go48GbIBY4/GGbz0DbGf+KSDeef8wxKYhbKBqqedYFRvkDG3AlPD",
    "ssxmod_itna2": "Yq+xniDQi=G=itXK0Lx0pm1QoGkDunBplxGuRq2KxikjoDl24QFQ08D+pYD=",
    "Hm_lpvt_5fd2e010217c332a79f6f3c527df12e9": "1736170386"
}
url = "https://www.vcg.com/api/creative/setsSearch"
data = {
    "category": 1197
}
data = json.dumps(data, separators=(',', ':'))

response = requests.post(url, headers=headers, cookies=cookies, data=data)
response.raise_for_status()  # 检查请求是否成功
response_json = response.json()

picture_list = response_json['list']
for picture in picture_list:
    picture_url = 'https:' + picture['src_0']
    print(picture_url)

    # 获取图片内容
    response = requests.get(picture_url)
    if response.status_code == 200:
        # 确保保存目录存在
        save_dir = 'dataset/downloaded_images'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 提取文件名
        file_name = os.path.basename(picture_url)
        save_path = os.path.join(save_dir, file_name)

        # 保存图片到本地
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"图片已保存到 {save_path}")
    else:
        print(f"无法下载图片 {picture_url}")






