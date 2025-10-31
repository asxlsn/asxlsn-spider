import base64
import json

import ddddocr
import execjs
import requests


class Spider:
    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://xxgs.chinanpo.mca.gov.cn/gsxt/newList",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        self.cookies = {
            "https_waf_cookie": "b4ca775f-8df6-4d7493f0aa37df3d33aac2166a8db04e98b3",
            "SF_cookie_129": "85115957"
        }
        self.url = "https://xxgs.chinanpo.mca.gov.cn/gsxt/PlatformSHZZFRKGSXT/slideCaptcha"

    def get_Image(self):
        """

        解析返回的JSON数据，提取a、b参数和两张图片(base64编码)
        保存为cutImage.png(滑块)和oriImage.png(背景)文件

        向服务器请求滑动验证码相关信息
        解析返回的JSON数据，提取关键参数a、b和两张验证码图片
        将base64编码的图片数据解码并保存为本地文件
        """
        try:
            response = requests.get(self.url, headers=self.headers, cookies=self.cookies)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()  # 直接解析为JSON
            result = data.get('result', {})
            if not result:
                raise ValueError("Response does not contain 'result' field")

            a = result.get('a')
            b = result.get('b')
            cutImage = result.get('c', {}).get('cutImage')
            oriImage = result.get('c', {}).get('oriImage')

            if not all([a, b, cutImage, oriImage]):
                raise ValueError("Missing required fields in response")

            # 保存图片文件
            with open('cutImage.png', 'wb') as f1, open('oriImage.png', 'wb') as f2:
                f1.write(base64.b64decode(cutImage))
                f2.write(base64.b64decode(oriImage))

            return a, b
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None, None
        except (ValueError, KeyError) as e:
            print(f"数据解析失败: {e}")
            return None, None

    def get_xcode(self):
        """
        识别滑块位置

        使用ddddocr库进行图像识别
        通过slide_match方法匹配滑块在背景图中的位置
        返回X轴坐标值，用于后续验证
        """
        det = ddddocr.DdddOcr(det=True, ocr=True, show_ad=False)
        with open('cutImage.png', 'rb') as f1, open('oriImage.png', 'rb') as f2:
            target_bytes = f1.read()
            background_bytes = f2.read()
        res = det.slide_match(target_bytes, background_bytes, simple_target=True)['target'][0]
        print("验证码识别结果：", res)
        return res


    def get_params(self, a, b, xcode):
        """
        参数加密处理
        读取本地的JavaScript文件excode.js
        使用execjs执行JS代码，模拟网站的加密逻辑
        生成验证所需的参数a、b、c
        """
        js_code = execjs.compile(open('excode.js', 'r', encoding='utf-8').read())
        result = js_code.call('getParams', a, b, xcode)
        return result


    def get_check(self, params):
        """
        验证码校验

        将加密后的参数发送到验证接口
        完成滑动验证码的校验过程
        """
        params = {
            "a": params.get('a'),
            "b": params.get('b'),
            "c": params.get('c')
        }
        print(params)
        response = requests.get(url="https://xxgs.chinanpo.mca.gov.cn/gsxt/PlatformSHZZFRKGSXT/slide_captcha_check",
                                params=params, headers=self.headers, cookies=self.cookies)
        return response.json()
        print("获取验证码结果"+response.json())

    def get_data(self,params):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://xxgs.chinanpo.mca.gov.cn",
            "Pragma": "no-cache",
            "Referer": "https://xxgs.chinanpo.mca.gov.cn/gsxt/newList",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        cookies = {
            "https_waf_cookie": "b4ca775f-8df6-4d7493f0aa37df3d33aac2166a8db04e98b3",
            "SF_cookie_129": "85115957"
        }
        url = "https://xxgs.chinanpo.mca.gov.cn/gsxt/PlatformSHZZFRKGSXT/biz/ma/shzzgsxt/a/gridQuery.html"
        data = {
            "pageNo": 1,
            "pageSize": 10,
            "paramsValue": "腾讯",
            "ssfw": "1",
            "aaae0127": "",
            "xyzk": "",
            "aaae0129": "",
            "aaae0105": "",
            "aaae0123": "",
            "aaae0114": "",
            "aae15having": "",
            "aaae0145": "",
            "aaae0110": "",
            "aaae0137": "",
            "aaae0149": "",
            "aaae0136": "",
            "aaae0139": "",
            "a": params.get('a'),
            "b": params.get('b'),
            "c": params.get('c')
        }
        data = json.dumps(data, separators=(',', ':'))
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        print(response.json())



if __name__ == '__main__':
    spider = Spider()
    a, b = spider.get_Image()
    xcode = spider.get_xcode()
    params = spider.get_params(a, b, xcode)
    check = spider.get_check(params)
    json_data = spider.get_data(params)

