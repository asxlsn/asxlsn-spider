import openpyxl
import requests
import json

# Set headers and cookies for the request.txt
headers = {
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Origin": "https://www.ly.com",
    "Pragma": "no-cache",
    "Referer": "https://www.ly.com/flights/itinerary/oneway/CTU-PEK?from=%E6%88%90%E9%83%BD&to=%E5%8C%97%E4%BA%AC&date=2024-12-30&fromairport=&toairport=",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "accept": "application/json, text/plain, */*",
    "content-type": "application/json;charset=UTF-8",
    "refid": "14211945",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "tcplat": "1",
    "tcsectoken;": "",
    "tcsessionid": "nologin-1735384214483",
    "tctracerid": "nologin-1735384214483",
    "tcuserid;": "",
    "tcversion": "1.1.0",
    "user-dun": "x78xxxxxIWWNNJNxIxAirETOjAN8gxCYhl8dWX7o85pxd58zHH0q67FNx0a/F3GexxxRvSrMvwzWV7OBYISOVUdVbp+O2ydltC/9SzB+KLIYvzxmttJK5YBkEpnQ5VjjKTFh0VOdttu8vVBmgSuN4N/xXOdK9B6tEpoQ3gMqtDDVS2R+gSrb2zD5YBgV0wsRHdjOgohVTVmKVXhiYB5+VIpiCIPOtjtxpkZjegHrlvs7KB/rTZ+1KQAukPQ00fsCzFh4kUDiD+hoxeK3vc04dBPasuRoFNAH5BuTVe9rpBSOTq28Y2hFGB5JHs+xaxpY",
}

cookies = {
    "NewProvinceId": "26",
    "NCid": "333",
    "NewProvinceName": "%E5%9B%9B%E5%B7%9D",
    "NCName": "%E7%BB%B5%E9%98%B3",
    "17uCNRefId": "RefId=14211945&SEFrom=bing&SEKeyWords=",
    "TicketSEInfo": "RefId=14211945&SEFrom=bing&SEKeyWords=",
    "CNSEInfo": "RefId=14211945&tcbdkeyid=&SEFrom=bing&SEKeyWords=&RefUrl=https%3A%2F%2Fcn.bing.com%2F",
    "qdid": "35297|1|14211945|dd62ba",
    "Hm_lvt_64941895c0a12a3bdeb5b07863a52466": "1735384077",
    "Hm_lpvt_64941895c0a12a3bdeb5b07863a52466": "1735384077",
    "HMACCOUNT": "EBE9CFC819B489FB",
}

url = "https://www.ly.com/flights/api/getflightlist"

# Data for the request.txt
data = {
    "Departure": "CTU",
    "Arrival": "PEK",
    "GetType": "1",
    "QueryType": "1",
    "fromairport": "",
    "toairport": "",
    "DepartureDate": "2025-22-30",
    "DepartureName": "成都",
    "ArrivalName": "北京",
    "IsBaby": 0,
    "paging": {
        "cid": "79e791c4-a885-4eb8-b705-aceb19c32532",
        "dataflag": "some"
    },
    "DepartureFilter": "",
    "ArrivalFilter": "",
    "flat": 1,
    "plat": 1,
    "isFromKylin": 1,
    "refid": "14211945"
}

data = json.dumps(data, separators=(',', ':'))

# Send POST request.txt
try:
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")
    exit()


wb = openpyxl.Workbook()
ws = wb.active
ws.append(["航空公司", "起飞机场", "起飞时间", "到达时间", "到达机场", "价格区间", "经历时长"])


flight_data = response.json().get("body", {}).get("FlightInfoSimpleList", [])

if not flight_data:
    print("不存在航班信息.")
else:
    for flight in flight_data:
        try:
            # 提取航班信息
            air_company_name = flight['airCompanyName']
            aapname = flight["aapname"]
            flight_time = flight['flyOffTime']
            end_time = flight['arrivalTime']
            otsn_name = flight['otsn']

            # 处理价格问题
            prices_flight = flight['productPrices']
            if isinstance(prices_flight, dict):
                prices_flight = str(prices_flight)  # Convert dictionary to string, or extract specific value if needed

            spantime = flight["spantime"]

            # 写入文件
            ws.append([air_company_name, aapname, flight_time, end_time, otsn_name, prices_flight, spantime])

            # 打印输出
            print(
                f"航空公司: {air_company_name}, 起飞时间: {flight_time}, 起飞机场: {aapname}, 到达时间: {end_time}, 到达机场: {otsn_name}, 价格区间: {prices_flight}, 经历时长: {spantime}")

        except KeyError as e:
            print(f"航班数据丢失: {e}")

# Save the workbook
wb.save("同城旅行-便宜机票.xlsx")
print("写入完成.")
