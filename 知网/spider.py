import json
import time

import requests
from bs4 import BeautifulSoup


import re

def sanitize_filename(name):
    if not name:
        return "untitled"
    # 替换 Windows 不允许的字符： \ / : * ? " < > |
    return re.sub(r'[\\/:*?"<>|]', "_", name)

headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "Ecp_ClientId=f250805123200186447; _c_WBKFRo=9VGjDG5LfO1dGKTzXxTH3pU89jm9e0zOiVwvJHT8; Ecp_session=1; SID_sug=018110; SID_kns_new=kns2618110; knsadv-searchtype=%7B%22BLZOG7CK%22%3A%22gradeSearch%2CmajorSearch%22%2C%22MPMFIG1A%22%3A%22gradeSearch%2CmajorSearch%2CsentenceSearch%22%2C%22T2VC03OH%22%3A%22gradeSearch%2CmajorSearch%22%2C%22JQIRZIYA%22%3A%22gradeSearch%2CmajorSearch%2CsentenceSearch%22%2C%22S81HNSV3%22%3A%22gradeSearch%22%2C%22YSTT4HG0%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22ML4DRIDX%22%3A%22gradeSearch%2CmajorSearch%22%2C%22WQ0UVIAA%22%3A%22gradeSearch%2CmajorSearch%22%2C%22VUDIXAIY%22%3A%22gradeSearch%2CmajorSearch%22%2C%22NN3FJMUV%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22LSTPFY1C%22%3A%22gradeSearch%2CmajorSearch%2CsentenceSearch%22%2C%22HHCPM1F8%22%3A%22gradeSearch%2CmajorSearch%22%2C%22OORPU5FE%22%3A%22gradeSearch%2CmajorSearch%22%2C%22WD0FTY92%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22BPBAFJ5S%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22EMRPGLPA%22%3A%22gradeSearch%2CmajorSearch%22%2C%22PWFIRAGL%22%3A%22gradeSearch%2CmajorSearch%2CsentenceSearch%22%2C%22U8J8LYLV%22%3A%22gradeSearch%2CmajorSearch%22%2C%22R79MZMCB%22%3A%22gradeSearch%22%2C%22J708GVCE%22%3A%22gradeSearch%2CmajorSearch%22%2C%22HR1YT1Z9%22%3A%22gradeSearch%2CmajorSearch%22%2C%22JUP3MUPD%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22NLBO1Z6R%22%3A%22gradeSearch%2CmajorSearch%22%2C%22RMJLXHZ3%22%3A%22gradeSearch%2CmajorSearch%2CsentenceSearch%22%2C%221UR4K4HZ%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22NB3BWEHK%22%3A%22gradeSearch%2CmajorSearch%22%2C%22XVLO76FD%22%3A%22gradeSearch%2CmajorSearch%22%7D; dblang=both; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IlhOMDA5NCIsIklkZW5JZCI6IldFRXZSRWN3U2xKSFNsZFNkbVZwYUU5aFJEQjROeXQ2WjI1c01rTm1aWFptTDBsd05HYzJWWEZSTUQwPSQ5QTRoRl9ZQXV2UTVvYmdWQXFOS1BDWWNFaktlbnNXNElRTW92d0h0d2tGNFZZUG9IYkt4SnchISIsIlBlcnNvblVzZXJOYW1lIjoiIiwiSW5zdFVzZXJOYW1lIjoiWE4wMDk0IiwiSW5zdFNob3dOYW1lIjoi5Zub5bed55yB5Yac5Lia56eR5a2m6Zmi5Yac5Lia5L-h5oGv5LiO5Yac5p2R57uP5rWO56CU56m25omAIiwibmJmIjoxNzU2MjYyMTMxLCJleHAiOjE3NTYyNzY1MzEsImlhdCI6MTc1NjI2MjEzMX0.1Oo296ngD4kdjf0I1NzgWAYE9iheOofoOROF7QEerVQ; tfstk=gUUtv-j3q9XgWR9w6-jHiGe0Ze5hxMVaORPWoxDMcJeLK5nbSS2GkkeLeED_shDYDRwtC1W4sZEYIS8miGk0HmNjK-Y0s-DLpVz3jEDGQqFbEqBlEabu_5uElTXkAkq0VqGfoxsnfqJL9pXlEabhyIRf4T20NS4_OjkI1fTsh63IwvG6h-MsApG-aqMbh-gIdfcDffM6lHTILjgjh-gf9WMEMqMbhq1LObcW6xAsHEEOFlweaLuwlEaK6Ds31v_TZyhTcYN_-ETXVfntF5MdC4D28DNqDrR2kmP_4-l7Cd6obSZLpf3A-hg79ow-TP_kBXrgO-kQwILz_VULJoid1NNKWAnuW0OvfVEbQrnaXI5zOVwU4Yo1Y9lLSzmxUDpCCWVKC0EYI98jIuFQp04HKU04LowjMJ9O4bauy0nXEYhDf6Cp0nosT868TMsBjjQE9YfHxn-qxXlKE6Cp0nosTXHltax20DcF.; SID_restapi=018105; LID=WEEvREcwSlJHSldSdmVpaE9hRDB4Nyt6Z250U2EvYzVYaVc1MzYxc0FYWT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw\\u0021\\u0021; Ecp_notFirstLogin=Qcn1vv; Ecp_LoginStuts={\"IsAutoLogin\":false,\"UserName\":\"XN0094\",\"ShowName\":\"%E5%9B%9B%E5%B7%9D%E7%9C%81%E5%86%9C%E4%B8%9A%E7%A7%91%E5%AD%A6%E9%99%A2%E5%86%9C%E4%B8%9A%E4%BF%A1%E6%81%AF%E4%B8%8E%E5%86%9C%E6%9D%91%E7%BB%8F%E6%B5%8E%E7%A0%94%E7%A9%B6%E6%89%80\",\"UserType\":\"bk\",\"BUserName\":\"\",\"BShowName\":\"\",\"BUserType\":\"\",\"r\":\"Qcn1vv\",\"Members\":[]}; c_m_LinID=LinID=WEEvREcwSlJHSldSdmVpaE9hRDB4Nyt6Z250U2EvYzVYaVc1MzYxc0FYWT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw\\u0021\\u0021&ot=08%2F27%2F2025%2012%3A23%3A26; c_m_expire=2025-08-27%2012%3A23%3A26",
    "Origin": "https://kns.cnki.net",
    "Pragma": "no-cache",
    "Referer": "https://kns.cnki.net/kns8s/defaultresult/index?crossids=YSTT4HG0%2CLSTPFY1C%2CJUP3MUPD%2CMPMFIG1A%2CWQ0UVIAA%2CBLZOG7CK%2CPWFIRAGL%2CEMRPGLPA%2CNLBO1Z6R%2CNN3FJMUV&korder=AF&kw=%E6%AD%A6%E6%B1%89%E5%A4%A7%E5%AD%A6",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
url = "https://kns.cnki.net/kns8s/brief/grid"
data = {
    "boolSearch": "true",
    "QueryJson": "{\"Platform\":\"\",\"Resource\":\"CROSSDB\",\"Classid\":\"WD0FTY92\",\"Products\":\"\",\"QNode\":{\"QGroup\":[{\"Key\":\"Subject\",\"Title\":\"\",\"Logic\":0,\"Items\":[{\"Field\":\"AF\",\"Value\":\"武汉大学\",\"Operator\":\"FUZZY\",\"Logic\":0,\"Title\":\"作者单位\"}],\"ChildItems\":[]}]},\"ExScope\":1,\"SearchType\":2,\"Rlang\":\"CHINESE\",\"KuaKuCode\":\"YSTT4HG0,LSTPFY1C,JUP3MUPD,MPMFIG1A,WQ0UVIAA,BLZOG7CK,PWFIRAGL,EMRPGLPA,NLBO1Z6R,NN3FJMUV\",\"Expands\":{},\"SearchFrom\":1}",
    "pageNum": "1",
    "pageSize": "20",
    "dstyle": "listmode",
    "boolSortSearch": "false",
    "productStr": "YSTT4HG0,LSTPFY1C,RMJLXHZ3,JQIRZIYA,JUP3MUPD,1UR4K4HZ,BPBAFJ5S,R79MZMCB,MPMFIG1A,WQ0UVIAA,NB3BWEHK,XVLO76FD,HR1YT1Z9,BLZOG7CK,PWFIRAGL,EMRPGLPA,J708GVCE,ML4DRIDX,NLBO1Z6R,NN3FJMUV,",
    "aside": "作者单位：武汉大学",
    "searchFrom": "资源范围：总库",
    "subject": "",
    "language": "",
    "uniplatform": "",
    "CurPage": "1"
}

response = requests.post(url, headers=headers, data=data)

html = response.text
soup = BeautifulSoup(html, "lxml")
# 找到论文列表表格
table = soup.find("table", class_="result-table-list")
if not table:
    print("没有找到结果表格")
else:
    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else []

    for row in rows:
        # 标题
        td_name = row.find("td", class_="name")
        if td_name:
            a_tag = td_name.find("a")
            if a_tag:
                title = a_tag.get_text(strip=True)
                href = a_tag.get("href")



        # 作者
        td_author = row.find("td", class_="author")
        authors = []
        if td_author:
            for a_tag in td_author.find_all("a", class_="KnowledgeNetLink"):
                authors.append(a_tag.get_text(strip=True))

        #来源
            # 来源
            td_source = row.find("td", class_="source")
            source = ""
            if td_source:
                a_tag = td_source.find("a")
                if a_tag:
                    source = a_tag.get_text(strip=True)





