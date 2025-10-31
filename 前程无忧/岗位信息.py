import time

import openpyxl
import requests

# 排除经验/学历类标签关键词
exclude_keywords = ["年", "经验", "实习", "大专", "本科", "研究生", "学历", "及以上", "应届", "在校", "中专", "专科"]

def clean_tags(tags):
    return [tag for tag in tags if not any(kw in tag for kw in exclude_keywords)]

def fetch_jobs(page_num=1):
    url = "https://we.51job.com/api/job/search-pc"
    params = {
        "api_key": "51job",
        "timestamp": time.time() * 1000,
        "keyword": "运维工程师",
        "searchType": "2",
        "jobArea": "090200",
        "pageNum": str(page_num),
        "pageSize": "20",
        "requestId": "cf89c033ac308e1d16b963367a6766bf",
        "accountId": "229877099",
        "pageCode": "sou|sou|soulb",
        "scene": "7"
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "account-id": "229877099",
        "cache-control": "no-cache",
        "from-domain": "51job_web",
        "partner": "www_google_com_hk",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "property": "%7B%22partner%22%3A%22www_google_com_hk%22%2C%22webId%22%3A2%2C%22fromdomain%22%3A%2251job_web%22%2C%22frompageUrl%22%3A%22https%3A%2F%2Fwe.51job.com%2F%22%2C%22pageUrl%22%3A%22https%3A%2F%2Fwe.51job.com%2Fpc%2Fsearch%3FjobArea%3D090200%26keyword%3D%25E8%25BF%2590%25E7%25BB%25B4%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588%26searchType%3D2%26keywordType%3D%22%2C%22identityType%22%3A%22%E5%9C%A8%E6%A0%A1%E7%94%9F%22%2C%22userType%22%3A%22%E8%80%81%E7%94%A8%E6%88%B7%22%2C%22isLogin%22%3A%22%E6%98%AF%22%2C%22accountid%22%3A%22229877099%22%2C%22keywordType%22%3A%22%22%7D",
        "referer": "https://we.51job.com/pc/search?jobArea=090200&keyword=%E8%BF%90%E7%BB%B4%E5%B7%A5%E7%A8%8B%E5%B8%88&searchType=2&keywordType=",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sign": "8c0eb42527e67863c423816738f2d581733bc6f7bbdb9d8ac89c80fe3afbdc89",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "user-token": "7d1fdb25d78648f691cf410d8e737789686283a4",
        "uuid": "3ccbb04d9f64b05851162ff35df6237a"
    }
    cookies = {
        "_c_i_p": "090200",
        "guid": "3ccbb04d9f64b05851162ff35df6237a",
        "ps": "needv%3D0",
        "51job": "cuid%3D229877099%26%7C%26cusername%3DrndFzaq2bpuYACyu9okgSJQsXiNW%252F57nEAQ5qtit2kg%253D%26%7C%26cpassword%3D%26%7C%26cname%3DovhSu33gqyX5lpxZ%252FrESWw%253D%253D%26%7C%26cemail%3D3%252FUjvfG3YWgpiFQ6VHBZVA%253D%253D%26%7C%26cemailstatus%3D0%26%7C%26cnickname%3D%26%7C%26ccry%3D.0hr.DT6cReeg%26%7C%26cconfirmkey%3Das4A%252FJTLDCTR6%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3Das5O..8D7%252FLAM%26%7C%26to%3D7d1fdb25d78648f691cf410d8e737789686283a4%26%7C%26",
        "sensor": "createDate%3D2023-06-29%26%7C%26identityType%3D2",
        "Hm_lvt_1370a11171bd6f2d9b1fe98951541941": "1751286556,1751334638",
        "HMACCOUNT": "29C8E5B0264CE645",
        "partner": "www_google_com_hk",
        "seo_refer_info_2023": "%7B%22referUrl%22%3A%22https%3A%5C%2F%5C%2Fwww.google.com.hk%5C%2F%22%2C%22referHost%22%3A%22www.google.com.hk%22%2C%22landUrl%22%3A%22https%3A%5C%2F%5C%2Fwww.51job.com%5C%2F%22%2C%22landHost%22%3A%22www.51job.com%22%2C%22partner%22%3A%22www_google_com_hk%22%7D",
        "Hm_lpvt_1370a11171bd6f2d9b1fe98951541941": "1751334650",
        "acw_tc": "ac11000117513346513365837e007ff17343cc8a6d5aa44dc794c5d8d45874",
        "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%22229877099%22%2C%22first_id%22%3A%22197c0d039035b9-02a0c3877ad67e-26011951-1327104-197c0d03904397%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com.hk%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk3YzBkMDM5MDM1YjktMDJhMGMzODc3YWQ2N2UtMjYwMTE5NTEtMTMyNzEwNC0xOTdjMGQwMzkwNDM5NyIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjIyOTg3NzA5OSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22229877099%22%7D%2C%22%24device_id%22%3A%22197c0d0ecd6dfd-05cb892a59c20e-26011951-1327104-197c0d0ecd71133%22%7D",
        "slife": "securetime%3DAj5SZlMwUDUDYg8yCjULZlBmAj0%253D",
        "acw_sc__v2": "68633f047ed140d0052f8b2cf2ba7596d382fb0f",
        "JSESSIONID": "0118239694F1F93A1B6B1A9C791B76C0",
        "ssxmod_itna": "iq+xRDcmG=0QDQGCDhr+GkDwZDm6+eTTDzxC5iOD+xQ5508D67DBbul4yY2P4rTuGPY/gTyqDBAqDseiQ4GzDiqKGhDBnY7qt/iy+dNScwEhdGn=ChRwdKjUhxpGkAlr1IqNUFBAKwDCPDExGk0EwxwDiiFx0rD0eDPxDYDG+aD7PDoxDrOIYDjYoICSEmQz4DKx0kDYHKv73DWxDFbb04dlGm2K7pNDDzNYlqK7xxDm+mkKYLvmxDnc0IeiGmD7y3DlP4OLdD0E=yNeSIbTZ232Aff40OD0KjOt7KuWgA1IB2w7GklNbHKYoYGo=GD5o4qBx=A=MMdHDYMBDAgxKlxNjGSBsOjdDD3wiGrjD=FDrfU9xNooNS=4xz5MlR/CxqmdejGw7IrBm1nwsemdl0xehCKhYnKOfD=FixD",
        "ssxmod_itna2": "iq+xRDcmG=0QDQGCDhr+GkDwZDm6+eTTDzxC5iOD+xQ5508D67DBbul4yY2P4rTuGPY/gTyqDBQ4DWwFCe2YzKDj44oToCBBqDlhD2n5T5n6x72mgbiQSUWoQ7SpPCskYt+wCHGpy7yHYHqTciecr0W0Cnsc=YQ2pFqWEYwx3K4qAI7y27eT2O8i/iC=CnPfpAxYSDfN4Ke6zy+f+iLMi7qcpSPxb04v4KppRc+0Bdw0pYxdFD23w785AQ7EOG7RBOh=I7hYwYQI2Bmfb76Hd18HXYICOC++9UwWpIT7ZWa4Egn+HQIY5jxBTnKqweq+t+ztHk8HCm2lS+Q4eBz7MRTfGKe5GvCH8QIpYmhDvRmTIznMYnEAeQBu0QEoki3kADupYsOYV9GGoHUFtoiMIWt=iM0oUK8+eYeVIDNcPiTeFnRzi3rnIFD1m2r/K4fvPFDe=asYeeVDFzP=w0LFWqlE2KDzYP=NGDuKkXiNd3QKRvRK=peFRIi=K74ejQYFKi6Bw8Pfc/eEfpxYCt=nR3L7cv8ucGWLNrmxz4+/2vcv27o1Q0KHDanFmN3ElO2FdhefFXj2U9fqja4ujk5Y0btdgr+wnGcw41XEeC=Sf=WwspihECS6jOOI4BWRIkBqnaq2M=s46ih8XpI7FLHBZXWuGtVEQiM2ptD+eKxe0R8UnqQYZ=mjuR/aPxB02Pyy8DewhH17rinhY5YmAGrDp6osKhQDGP4pNO2vWhDxKzxw0YlD+Yo4PMiNlqxxXDerDot+=Gd3DD"
    }

    resp = requests.get(url, headers=headers, cookies=cookies, params=params)
    return resp.json().get("resultbody", {}).get("job", {}).get("items", [])


def auto_adjust_column_width(ws):
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # 列字母，比如 'A', 'B', 'C'...
        for cell in col:
            if cell.value:
                # 这里转成字符串计算长度，中文会占2个字符宽度左右，所以简单*1.2放大一点
                length = int(len(str(cell.value)) * 1.2)
                if length > max_length:
                    max_length = length
        # 设置最大宽度，防止过大可以限定最大宽度，比如 50
        adjusted_width = min(max_length, 50)
        ws.column_dimensions[column].width = adjusted_width

def write_jobs_to_excel(filename="职位信息列表.xlsx", total_pages=1):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "职位列表"

    # 写入表头
    ws.append([
        "职位名称", "公司名称", "工作地点", "最低薪资", "最高薪资",
        "学历要求", "经验要求", "职位标签", "岗位职责"
    ])

    for page in range(1, total_pages + 1):
        print(f"抓取第 {page} 页...")
        job_items = fetch_jobs(page)

        for job in job_items:
            tags = clean_tags(job.get("jobTags", []))
            row = [
                job.get("jobName", ""),
                job.get("companyName", ""),
                job.get("jobAreaString", ""),
                job.get("jobSalaryMin", ""),
                job.get("jobSalaryMax", ""),
                job.get("degreeString", ""),
                job.get("workYearString", ""),
                ", ".join(tags),
                job.get("jobDescribe", "").replace("\n", " ").strip()[:100]
            ]
            ws.append(row)
    # 写完所有数据后，调用自动调整函数
    auto_adjust_column_width(ws)

    wb.save(filename)
    print(f"保存完成：{filename}")

# === 调用函数 ===
write_jobs_to_excel(total_pages=33)
