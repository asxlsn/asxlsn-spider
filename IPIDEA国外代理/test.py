import requests
from bs4 import BeautifulSoup
import time

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Referer": "https://www150.statcan.gc.ca/n1/en/type/analysis?p=2-All",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
cookies = {
    "AMCVS_A90F2A0D55423F537F000101%40AdobeOrg": "1",
    "gpv_pthl": "blank%20theme",
    "gpv_pc": "Government%20of%20Canada%2C%20Statistics%20Canada",
    "s_cc": "true",
    "AMCV_A90F2A0D55423F537F000101%40AdobeOrg": "-1124106680%7CMCIDTS%7C20109%7CMCMID%7C68784573784261235170938892308245871786%7CMCAAMLH-1737975110%7C3%7CMCAAMB-1737975110%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1737377511s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.2.0",
    "gpv_pu": "www150.statcan.gc.ca%2Fn1%2Fen%2Ftype%2Fanalysis",
    "gpv_pt": "Analysis",
    "gpv_url": "www150.statcan.gc.ca%2Fn1%2Fen%2Ftype%2Fanalysis",
    "gpv_pqs": "%3Fp%3D2-all",
    "s_ips": "1219.7999877929688",
    "s_tp": "3920",
    "s_plt": "4.28",
    "s_ppv": "Analysis%2C100%2C31%2C3918%2C26%2C26",
    "s_sq": "canadalivemain%3D%2526c.%2526a.%2526activitymap.%2526page%253DAnalysis%2526link%253D1%252520Go%252520to%252520page%2525201%252520of%252520All%252520results%2526region%253Dall%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c"
}


def testUrl():
    for page in range(0, 10):
        # 设置帐密代理
        proxy = {
            'http': 'http://huanghun-zone-custom:979269asx@d8e7474dfe723dd3.lqz.na.ipidea.online:2336',
            'https': 'http://huanghun-zone-custom:979269asx@d8e7474dfe723dd3.lqz.na.ipidea.online:2336',
        }
        try:
            mainUrl = f"https://www150.statcan.gc.ca/n1/en/type/analysis?p={page}-All#all"
            res = requests.get(mainUrl, headers=headers, cookies=cookies, proxies=proxy, timeout=10)
            soup = BeautifulSoup(res.text, "lxml")
            print("正在下载第" + str(page) + "页的数据...")
            for i, a in enumerate(soup.select("div.ndm-result-container > div.ndm-result-title > span a")[:10]):
                href = a['href']
                if href.endswith('.htm'):
                    pdf_url = href.replace('htm', 'pdf')
                else:
                    pdf_url = "https://www150.statcan.gc.ca" + href.replace('htm', 'pdf')

                res = requests.get(pdf_url, headers=headers, cookies=cookies, proxies=proxy, timeout=10)
                with open(f"{int(time.time() * 1000)}.pdf", "wb") as f:
                    f.write(res.content)
                print("下载成功")
        except Exception as e:
            print("访问失败", e)
            pass


if __name__ == '__main__':
    testUrl()
