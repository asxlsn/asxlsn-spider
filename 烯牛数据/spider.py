import execjs
import json
import requests


class XiniuSpider:
    def __init__(self, js_file="code.js"):
        # 读取并编译 JS
        with open(js_file, "r", encoding="utf-8") as f:
            js_code = f.read()
        self.ctx = execjs.compile(js_code)

        # 请求头
        self.headers = {
            "accept": "application/json",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "https://www.xiniudata.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.xiniudata.com/project/lib",
            "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }

        # Cookie 需按需更新
        self.cookies = {
            "btoken": "R013OTC5U69WCXQN07AOJPKKMARY530C",
            "utoken": "E7L0DK7I4QCN2IJPNP0DONL6BUO00BB7",
            "username": "%E4%BA%91%E8%BE%B9%E5%B0%8F%E9%95%87",
            "Hm_lvt_42317524c1662a500d12d3784dbea0f8": "1753866077,1755249489,1755273939",
            "HMACCOUNT": "29C8E5B0264CE645",
            "Hm_lpvt_42317524c1662a500d12d3784dbea0f8": "1755273993"
        }

    def encrypt(self, data: dict) -> dict:
        """调用 JS 加密"""
        result = json.loads(self.ctx.call("encryptData", data))
        result["v"] = 1
        return result

    def decrypt(self, data: str) -> dict:
        """调用 JS 解密"""
        return self.ctx.call("decryptData", data)

    def search_company(self, params: dict) -> list:
        """
        搜索公司
        params: dict，例如 {
            "industry_ids": 1659,
            "domestic": True,
            "corporate_locationIds": [],
            "tag_names": [],
            "corporate_rounds": [],
            "sort": 76006,
            "order": -1,
            "start": 20,
            "limit": 10
        }
        return: company_code 列表
        """
        url = "https://www.xiniudata.com/api/search3/company/search_company_for_lib"
        post_data = self.encrypt(params)
        response = requests.post(url, headers=self.headers, cookies=self.cookies, json=post_data).json()
        json_data = self.decrypt(response['d'])
        return [i['company_code'] for i in json_data['data']]

    def get_company_detail(self, company_codes: list) -> dict:
        """
        根据公司代码查询公司详情
        """
        url = "https://www.xiniudata.com/api2/service/x_service/person_company4_list/list_companies4_list_by_codes"
        post_data = self.encrypt({'codes': company_codes})
        response = requests.post(url, headers=self.headers, cookies=self.cookies, json=post_data).json()
        return self.decrypt(response['d'])


if __name__ == "__main__":
    spider = XiniuSpider()

    all_codes = []
    max_pages = 5  # 爬取前 5 页
    limit = 10  # 每页数量

    for page in range(max_pages):
        # 每次循环重新构造载荷
        search_params = {
            "industry_ids": 1659,
            "domestic": True,
            "corporate_locationIds": [],
            "tag_names": [],
            "corporate_rounds": [],
            "sort": 76006,
            "order": -1,
            "start": page * limit,  # 动态修改
            "limit": limit
        }

        codes = spider.search_company(search_params)
        if not codes:
            print(f"第 {page + 1} 页没有数据，提前结束")
            break

        print(f"第 {page + 1} 页获取到 {len(codes)} 条")
        all_codes.extend(codes)

    print("总公司数:", len(all_codes))

    # 查询公司详情
    detail = spider.get_company_detail(all_codes)
    print("公司详情:", detail)


