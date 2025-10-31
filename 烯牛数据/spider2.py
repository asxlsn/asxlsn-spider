import random
from typing import List, Dict, Any, Optional
import execjs
import json
import requests
from datetime import datetime
import time
import pandas as pd


class XiniuSpider:
    def __init__(self, js_file="code.js"):
        """初始化烯牛数据爬虫"""
        self.js_file = js_file
        self.ctx = self._init_js_context()
        self.headers = self._get_headers()
        self.cookies = self._get_cookies()
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _init_js_context(self):
        """初始化JS执行环境"""
        try:
            with open(self.js_file, "r", encoding="utf-8") as f:
                js_code = f.read()
            return execjs.compile(js_code)
        except FileNotFoundError:
            raise FileNotFoundError(f"找不到JS文件: {self.js_file}")
        except Exception as e:
            raise Exception(f"JS编译失败: {e}")

    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
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

    def _get_cookies(self) -> Dict[str, str]:
        """获取Cookie信息"""
        return {
            "btoken": "R013OTC5U69WCXQN07AOJPKKMARY530C",
            "utoken": "E7L0DK7I4QCN2IJPNP0DONL6BUO00BB7",
            "username": "%E4%BA%91%E8%BE%B9%E5%B0%8F%E9%95%87",
            "Hm_lvt_42317524c1662a500d12d3784dbea0f8": "1753866077,1755249489,1755273939",
            "HMACCOUNT": "29C8E5B0264CE645",
            "Hm_lpvt_42317524c1662a500d12d3784dbea0f8": "1755273993"
        }

    def update_cookies(self, cookies: Dict[str, str]):
        """更新Cookie"""
        self.cookies.update(cookies)

    def encrypt(self, data: dict) -> dict:
        """调用 JS 加密"""
        try:
            result = json.loads(self.ctx.call("encryptData", data))
            result["v"] = 1
            return result
        except json.JSONDecodeError as e:
            raise Exception(f"加密结果解析失败: {e}")
        except Exception as e:
            raise Exception(f"加密失败: {e}")

    def decrypt(self, data: str) -> dict:
        """调用 JS 解解密"""
        try:
            return self.ctx.call("decryptData", data)
        except Exception as e:
            raise Exception(f"解密失败: {e}")

    def search_company(self, params: dict) -> List[str]:
        """
        搜索公司
        params: 搜索参数
        return: company_code 列表
        """
        url = "https://www.xiniudata.com/api/search3/company/search_company_for_lib"
        try:
            post_data = self.encrypt(params)
            response = self.session.post(url, cookies=self.cookies, json=post_data, timeout=15)
            response.raise_for_status()

            response_json = response.json()
            if 'd' not in response_json:
                raise ValueError("响应中缺少'd'字段")

            json_data = self.decrypt(response_json['d'])

            if 'data' not in json_data:
                return []

            return [item['company_code'] for item in json_data['data'] if 'company_code' in item]
        except requests.RequestException as e:
            print(f"网络请求失败: {e}")
            return []
        except ValueError as e:
            print(f"数据解析失败: {e}")
            return []
        except Exception as e:
            print(f"搜索公司失败: {e}")
            return []

    def get_company_detail(self, company_codes: List[str]) -> List[Dict[str, Any]]:
        """
        根据公司代码查询公司详情
        """
        if not company_codes:
            return []

        url = "https://www.xiniudata.com/api2/service/x_service/person_company4_list/list_companies4_list_by_codes"
        try:
            post_data = self.encrypt({'codes': company_codes})
            response = self.session.post(url, cookies=self.cookies, json=post_data, timeout=15)
            response.raise_for_status()

            response_json = response.json()
            if 'd' not in response_json:
                raise ValueError("响应中缺少'd'字段")

            json_data = self.decrypt(response_json['d'])

            result = []
            data_list = json_data.get('list', [])

            for data in data_list:
                if not isinstance(data, dict):
                    continue

                # 安全获取字段值
                funding_info = data.get('funding') or {}
                if not isinstance(funding_info, dict):
                    funding_info = {}

                result.append({
                    '公司名称': self._safe_get_str(data, 'name'),
                    '赛道': self._safe_get_str(data, 'brief'),
                    '当前轮次': self._safe_get_str(data, 'roundName'),
                    '最新获投时间': funding_info.get('fundingDate'),
                    '成立时间': funding_info.get('publishDate'),
                    '行业领域': self._safe_get_list(data, 'tagNameList'),
                    '地点': self._safe_get_str(data, 'cityName'),
                })
            return result
        except requests.RequestException as e:
            print(f"网络请求失败: {e}")
            return []
        except ValueError as e:
            print(f"数据解析失败: {e}")
            return []
        except Exception as e:
            print(f"获取公司详情失败: {e}")
            return []

    @staticmethod
    def _safe_get_str(data: dict, key: str, default: str = '') -> str:
        """安全获取字符串值"""
        value = data.get(key)
        if value is None:
            return default
        return str(value) if value else default

    @staticmethod
    def _safe_get_list(data: dict, key: str, default: list = []) -> list:
        """安全获取列表值"""
        value = data.get(key)
        if not isinstance(value, list):
            return default.copy()
        return value

    @staticmethod
    def format_timestamp(timestamp: Optional[Any]) -> str:
        """格式化时间戳为日期字符串"""
        if not timestamp:
            return '无数据'

        try:
            # 转换为数值类型
            if isinstance(timestamp, str):
                timestamp = float(timestamp)

            # 如果是毫秒时间戳，转换为秒
            if isinstance(timestamp, (int, float)) and timestamp > 1000000000000:
                timestamp = timestamp / 1000

            # 确保是有效的时间戳
            if not isinstance(timestamp, (int, float)) or timestamp < 0:
                return '无效时间'

            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        except (ValueError, OSError, TypeError):
            return '无效时间'

    def print_company_details(self, details: List[Dict[str, Any]]) -> None:
        """打印公司详情"""
        if not details:
            print("没有公司详情数据")
            return

        print(f"获取到 {len(details)} 家公司详情：")
        print("=" * 120)
        # 打印表头
        print(f"{'序号':<4} {'公司名称':<25} {'赛道':<15} {'当前轮次':<10} {'地点':<10} {'成立时间':<12} {'获投时间':<12} {'行业领域'}")
        print("-" * 120)

        for i, detail in enumerate(details, 1):
            # 格式化时间
            funding_date = self.format_timestamp(detail['最新获投时间'])
            publish_date = self.format_timestamp(detail['成立时间'])

            # 格式化行业领域
            industry_fields = ', '.join(detail['行业领域']) if detail['行业领域'] else '无数据'

            # 安全处理可能为None的值
            company_name = detail.get('公司名称') or ''
            track = detail.get('赛道') or ''
            round_name = detail.get('当前轮次') or ''
            city = detail.get('地点') or ''

            print(f"{i:<4} {company_name:<25} {track:<15} {round_name:<10} {city:<10} "
                  f"{publish_date:<12} {funding_date:<12} {industry_fields}")

    def save_to_excel(self, details: List[Dict[str, Any]], filename: str = "烯牛数据.xlsx") -> None:
        """将公司详情保存到Excel文件"""
        if not details:
            print("没有数据可保存到Excel")
            return

        try:
            # 处理数据，将时间戳转换为可读日期
            processed_data = []
            for detail in details:
                processed_detail = detail.copy()
                # 格式化时间戳
                processed_detail['成立时间'] = self.format_timestamp(detail['成立时间'])
                processed_detail['最新获投时间'] = self.format_timestamp(detail['最新获投时间'])
                # 将行业领域列表转换为字符串
                if isinstance(detail['行业领域'], list):
                    processed_detail['行业领域'] = ', '.join(detail['行业领域']) if detail['行业领域'] else '无数据'
                processed_data.append(processed_detail)

            # 创建DataFrame
            df = pd.DataFrame(processed_data)

            # 保存到Excel文件
            df.to_excel(filename, index=False, engine='openpyxl')
            print(f"数据已保存到 {filename}")
        except Exception as e:
            print(f"保存Excel文件失败: {e}")

    def crawl_companies(self, industry_id: int = 1659, max_pages: int = 5, limit: int = 10) -> List[str]:
        """爬取公司代码"""
        all_codes = []
        print(f"开始搜索公司... (行业ID: {industry_id})")

        for page in range(max_pages):
            search_params = {
                "industry_ids": industry_id,
                "domestic": True,
                "corporate_locationIds": [],
                "tag_names": [],
                "corporate_rounds": [],
                "sort": 76006,
                "order": -1,
                "start": page * limit,
                "limit": limit
            }

            codes = self.search_company(search_params)
            if not codes:
                print(f"第 {page + 1} 页没有数据，提前结束")
                break

            print(f"第 {page + 1} 页获取到 {len(codes)} 条")
            all_codes.extend(codes)
            # 添加延时避免请求过于频繁
            # 添加随机延时(1-4秒)避免请求过于频繁
            delay = random.uniform(1, 4)
            print(f"等待 {delay:.1f} 秒...")
            time.sleep(delay)

        print(f"总共获取到 {len(all_codes)} 家公司")
        return all_codes


def main():
    """主函数"""
    try:
        spider = XiniuSpider()

        # 爬取公司代码
        company_codes = spider.crawl_companies(industry_id=1659, max_pages=10, limit=10)

        # 获取并打印公司详情
        if company_codes:
            print("\n开始获取公司详情...")
            details = spider.get_company_detail(company_codes)
            spider.print_company_details(details)

            # 保存到Excel文件
            spider.save_to_excel(details, "烯牛数据.xlsx")
        else:
            print("未获取到公司代码，无法获取详情")

    except Exception as e:
        print(f"程序执行出错: {e}")


if __name__ == "__main__":
    main()
