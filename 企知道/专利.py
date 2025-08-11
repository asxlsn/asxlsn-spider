import requests
import json
from Crypto.Cipher import AES
import base64
import openpyxl
from datetime import datetime

AES_KEYS = {
    1: "xc46VoB49X3PGYAg",
    2: "KE3pb84wxqLTZEG3",
    3: "18Lw0OEaBBUwHYNT",
    4: "jxxWWIzvkqEQcZrd",
    5: "40w42rjLEXxYhxRn",
    6: "K6hkD03WNW8N1fPM",
    7: "I8V3IwIhrwNbWxqz",
    8: "3JNNbxAP4zi5oSGA",
    9: "7pUuESQl8aRTFFKK",
    10: "KB4GAHN6M5soB3WV"
}


def aes_ecb_decrypt_base64(cipher_text: str, key_index: int) -> str:
    """
    AES ECB模式Base64解密并去除PKCS7填充
    """
    if key_index not in AES_KEYS:
        raise ValueError(f"无效的密钥编号：{key_index}")
    key = AES_KEYS[key_index].encode('utf-8')
    cipher_data = base64.b64decode(cipher_text)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(cipher_data)
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode('utf-8')


def format_timestamp(ms):
    if not ms:
        return ""
    return datetime.utcfromtimestamp(ms / 1000).strftime('%Y-%m-%d')


def write_qizhidao_patents_to_excel(json_str, excel_filename):
    """
    将启知数据专利 JSON 字符串写入 Excel 文件。
    """
    data = json.loads(json_str)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "专利数据"

    headers = [
        "id", "patent_name", "patent_name_en", "patent_name_zh", "patent_brief",
        "app_num_standard", "out_num", "out_type", "designer", "app_date", "out_date",
        "cur_legal_status", "valid_status", "claims_num", "receiving_office", "patent_img"
    ]
    ws.append(headers)

    for record in data.get("records", []):
        row = [
            record.get("id", ""),
            record.get("patent_name", ""),
            record.get("patent_name_en", ""),
            record.get("patent_name_zh", ""),
            record.get("patent_brief", ""),
            record.get("app_num_standard", ""),
            record.get("out_num", ""),
            record.get("out_type", ""),
            ", ".join(record.get("designer", [])) if record.get("designer") else "",
            format_timestamp(record.get("app_date")),
            format_timestamp(record.get("out_date")),
            record.get("cur_legal_status", ""),
            record.get("valid_status", ""),
            record.get("claims_num", ""),
            record.get("receiving_office", ""),
            record.get("patent_img", "")
        ]
        ws.append(row)

    wb.save(excel_filename)
    print(f"写入Excel完成，文件名：{excel_filename}")


def fetch_and_save_qizhidao_patents(page=1, excel_filename="qizhidao_patents.xlsx"):
    """
    发送请求，解密数据，写入Excel文件。
    page参数控制当前请求页码。
    """
    url = "https://app.qizhidao.com/qzd-bff-patent/patent/v2/search"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "accesstoken": "eyJhbGciOiJIUzUxMiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0UTBKRExVaFRNalUySW4wLi5jUmtMZndKWGhISUdpdW5DM0x4Z2ZRLjYtbmpGQXJBSDhuM01Zcy0zVkJyNGx6NTRsWjNkMTZiNW5objNsaFZoRV9lU0JnU2YzaGlRWDduTFh3cEtJUnhmMXZybGtSRmVPNGxnZ1pzazRRM3JXNjlfbndUUjdBdTdoeUh4NVZRTkdmWG9VVFRmT0k4NGJfaWRzalBwaENyRVExNWdFNHR2TFVXTE5RQTJRUGw5c0lzT2haeW50bHJBTU15UTBZX1JRbG01cktMeEVGd2hMb0xjR0FmaV96dGJCNVJRbGdZSHVIYjFfWkd5OXJMNEVWVWoxeld0VER4SDFBV3laNmlfRGcuS1NzSndKbGo2YllHRFJTcjdQM3VGZw.mnYj8Fu3jzieBZ7Z2TBIDcvk98fJsUis60RSyrEFePKsRo6rz8MdDokcC8b1GeFMrEmyjvYaBuCRIfBzmkR8BA",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "device-id": "BEQEYsd27lvqjrdA/NmjwqUGRIb+2PH/wkqKp8ozz3G6BYV4O2Z42OTBkWhIDJXM5A5KjO95aSNa0vvd1LA9YCg==",
        "h5version": "v1.0.0",
        "origin": "https://patents.qizhidao.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://patents.qizhidao.com/search/result?uid=key-1753410162280&from=simple&searchBtntype=searchBtn&searchType=simple_search&businessSource=PC%E6%9F%A5%E4%B8%93%E5%88%A9-%E5%B7%A6%E4%BE%A7%E6%90%9C%E7%B4%A2&statement=ASPS_EXACT%3A%28%22%E8%A5%BF%E5%8D%97%E8%B4%A2%E7%BB%8F%E5%A4%A7%E5%AD%A6%E5%A4%A9%E5%BA%9C%E5%AD%A6%E9%99%A2%22%29&resultForm=%E5%85%B6%E4%BB%961&scType=%E5%85%B6%E4%BB%961&collection=%E5%85%B6%E4%BB%961&current=1&filter=",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sensordeviceid": "1983f613e1a156a-0bae2da6cdc884-26011951-1327104-1983f613e1b1723",
        "sensorsdistinctid": "c0db24d8680b49b4a8678ad0a36910e8",
        "signature": "e0ec636e1838cbbdbf831d9a71758548.aRC00s",
        "token": "eyJhbGciOiJIUzUxMiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0UTBKRExVaFRNalUySW4wLi5jUmtMZndKWGhISUdpdW5DM0x4Z2ZRLjYtbmpGQXJBSDhuM01Zcy0zVkJyNGx6NTRsWjNkMTZiNW5objNsaFZoRV9lU0JnU2YzaGlRWDduTFh3cEtJUnhmMXZybGtSRmVPNGxnZ1pzazRRM3JXNjlfbndUUjdBdTdoeUh4NVZRTkdmWG9VVFRmT0k4NGJfaWRzalBwaENyRVExNWdFNHR2TFVXTE5RQTJRUGw5c0lzT2haeW50bHJBTU15UTBZX1JRbG01cktMeEVGd2hMb0xjR0FmaV96dGJCNVJRbGdZSHVIYjFfWkd5OXJMNEVWVWoxeld0VER4SDFBV3laNmlfRGcuS1NzSndKbGo2YllHRFJTcjdQM3VGZw.mnYj8Fu3jzieBZ7Z2TBIDcvk98fJsUis60RSyrEFePKsRo6rz8MdDokcC8b1GeFMrEmyjvYaBuCRIfBzmkR8BA",
        "traceparent": "00-1e130cebec2e4008ab9f6a35d8ddbb01-d6ae85f2c5e0d028-01",
        "tracestate": "rum=v2&browser&fyw9n1jhpf@18ff4c0a0d8fd8d&487c27a6f1804b00b898170d345e64c7&uid_tfxjlwhu0pc63iii",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "user-agent-web": "X/32ed80a37cf74a5697657feae2d62323"
    }
    cookies = {
        "sajssdk_2015_cross_new_user": "1",
        "acw_tc": "ac11000117534099479727928e0076b53bf40578ebc60f43f89c3ccca21820",
        "wz_uuid": "X/32ed80a37cf74a5697657feae2d62323",
        "Hm_lvt_9ea3e7293b7c088e0d2c88874b63e7dd": "1753409995",
        "HMACCOUNT": "29C8E5B0264CE645",
        "token": "eyJhbGciOiJIUzUxMiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0UTBKRExVaFRNalUySW4wLi5jUmtMZndKWGhISUdpdW5DM0x4Z2ZRLjYtbmpGQXJBSDhuM01Zcy0zVkJyNGx6NTRsWjNkMTZiNW5objNsaFZoRV9lU0JnU2YzaGlRWDduTFh3cEtJUnhmMXZybGtSRmVPNGxnZ1pzazRRM3JXNjlfbndUUjdBdTdoeUh4NVZRTkdmWG9VVFRmT0k4NGJfaWRzalBwaENyRVExNWdFNHR2TFVXTE5RQTJRUGw5c0lzT2haeW50bHJBTU15UTBZX1JRbG01cktMeEVGd2hMb0xjR0FmaV96dGJCNVJRbGdZSHVIYjFfWkd5OXJMNEVWVWoxeld0VER4SDFBV3laNmlfRGcuS1NzSndKbGo2YllHRFJTcjdQM3VGZw.mnYj8Fu3jzieBZ7Z2TBIDcvk98fJsUis60RSyrEFePKsRo6rz8MdDokcC8b1GeFMrEmyjvYaBuCRIfBzmkR8BA",
        "accessToken": "eyJhbGciOiJIUzUxMiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0UTBKRExVaFRNalUySW4wLi5jUmtMZndKWGhISUdpdW5DM0x4Z2ZRLjYtbmpGQXJBSDhuM01Zcy0zVkJyNGx6NTRsWjNkMTZiNW5objNsaFZoRV9lU0JnU2YzaGlRWDduTFh3cEtJUnhmMXZybGtSRmVPNGxnZ1pzazRRM3JXNjlfbndUUjdBdTdoeUh4NVZRTkdmWG9VVFRmT0k4NGJfaWRzalBwaENyRVExNWdFNHR2TFVXTE5RQTJRUGw5c0lzT2haeW50bHJBTU15UTBZX1JRbG01cktMeEVGd2hMb0xjR0FmaV96dGJCNVJRbGdZSHVIYjFfWkd5OXJMNEVWVWoxeld0VER4SDFBV3laNmlfRGcuS1NzSndKbGo2YllHRFJTcjdQM3VGZw.mnYj8Fu3jzieBZ7Z2TBIDcvk98fJsUis60RSyrEFePKsRo6rz8MdDokcC8b1GeFMrEmyjvYaBuCRIfBzmkR8BA",
        "creditNo": "%22%22",
        "param_sign": "0bsN5M",
        "x-web-ip": "182.143.130.154, 119.23.123.169, 47.106.31.162, 100.121.108.221",
        "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%22c0db24d8680b49b4a8678ad0a36910e8%22%2C%22first_id%22%3A%221983f6084ec1dd-0648c2f7a46a794-26011951-1327104-1983f6084ed15a5%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk4M2Y2MDg0ZWMxZGQtMDY0OGMyZjdhNDZhNzk0LTI2MDExOTUxLTEzMjcxMDQtMTk4M2Y2MDg0ZWQxNWE1IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiYzBkYjI0ZDg2ODBiNDliNGE4Njc4YWQwYTM2OTEwZTgifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22c0db24d8680b49b4a8678ad0a36910e8%22%7D%2C%22%24device_id%22%3A%221983f613e1a156a-0bae2da6cdc884-26011951-1327104-1983f613e1b1723%22%7D",
        "sensorsdata2015jssdkchannel": "%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D",
        "Hm_lpvt_9ea3e7293b7c088e0d2c88874b63e7dd": "1753410869"
    }
    data = {
        "text_ver": "",
        "subWordSwitch": None,
        "isApp": False,
        "sortColumns": None,
        "listColumns": [
            {
                "name": "公开(公告)号",
                "shortName": "PN",
                "columnName": "out_num"
            },
            {
                "name": "标题",
                "shortName": "TI",
                "columnName": "patent_name"
            },
            {
                "name": "摘要",
                "shortName": "ABS",
                "columnName": "patent_brief"
            },
            {
                "name": "摘要附图",
                "shortName": "IMAGE",
                "columnName": "patent_img"
            },
            {
                "name": "公开类型",
                "shortName": "PDT",
                "columnName": "out_type"
            },
            {
                "name": "原始申请人",
                "shortName": "AP",
                "columnName": "app_person"
            },
            {
                "name": "当前权利人",
                "shortName": "ASP",
                "columnName": "patent_person"
            },
            {
                "name": "原始发明(设计)人",
                "shortName": "IN",
                "columnName": "designer"
            },
            {
                "name": "申请日",
                "shortName": "AD",
                "columnName": "app_date"
            },
            {
                "name": "公开(公告)日",
                "shortName": "PD",
                "columnName": "out_date"
            },
            {
                "name": "当前法律状态",
                "shortName": "LSC",
                "columnName": "cur_legal_status"
            },
            {
                "name": "法律事件",
                "shortName": "LGE",
                "columnName": "legal_event"
            },
            {
                "name": "申请号",
                "shortName": "AN",
                "columnName": "app_num_standard"
            },
            {
                "name": "IPC分类号",
                "shortName": "IPC",
                "columnName": "ipc"
            },
            {
                "name": "LOC分类号",
                "shortName": "LC",
                "columnName": "loc"
            },
            {
                "name": "授权公告日",
                "shortName": "GRANT_D",
                "columnName": "authorize_date"
            },
            {
                "name": "申请号",
                "shortName": "AN",
                "columnName": "app_num_standard"
            },
            {
                "name": "专利有效性",
                "shortName": "STATUS",
                "columnName": "valid_status"
            }
        ],
        "columnType": 1,
        "secondFlag": False,
        "searchType": "simple_search",
        "current": page,
        "pageSize": 20,
        "statement": "ASPS_EXACT:(\"西南科技大学\")",
        "filter": "",
        "pageCount": 0,
        "checkResult": True,
        "featureCode": "patents_pro_search",
        "businessKey": "ASPS_EXACT:(\"西南科技大学\")",
        "highlightSource": 1
    }



    try:
        response = requests.post(url, headers=headers, cookies=cookies, json=data, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print("请求接口失败:", e)
        return False

    try:
        res_json = response.json()
    except Exception as e:
        print("响应非JSON格式:", e)
        return False

    cipher_data = res_json.get("data1")
    if not cipher_data:
        print("响应中未找到加密字段 data1")
        return False

    key_index = res_json.get("hasUse", 4)
    print(f"使用密钥编号：{key_index}")

    try:
        plaintext = aes_ecb_decrypt_base64(cipher_data, key_index)
        print("解密成功，写入Excel中...")
        write_qizhidao_patents_to_excel(plaintext, excel_filename)
        return True
    except Exception as e:
        print("解密失败:", e)
        return False


if __name__ == "__main__":
    if __name__ == "__main__":
        for page_num in range(1, 2):  # 1到5页
            filename = f"专利数据_page{page_num}.xlsx"
            print(f"开始抓取第 {page_num} 页数据...")
            success = fetch_and_save_qizhidao_patents(page=page_num, excel_filename=filename)
            if not success:
                print(f"第 {page_num} 页抓取失败，停止抓取。")
                break

