import time

import requests
import json

from loguru import logger

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "http://www.ccgp-qinghai.gov.cn",
    "Pragma": "no-cache",
    "Referer": "http://www.ccgp-qinghai.gov.cn/site/category?parentId=4149&childrenCode=ZcyAnnouncement&utm=luban.luban-PC-43180.959-pc-websitegroup-navBar-front.3.e24852a098f711f0812a3d659e05ee20",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}
cookies = {
    "acw_tc": "1a0c599a17587797768807201e9e7b1a11cb6db7816b6c1735a75f61f35767",
    "_zcy_log_client_uuid": "5b56b150-99d4-11f0-b421-edd0ab2298ef",
    "acw_sc__v2": "197d84838-b9345f782b85dbcf2beb14193602a1a5465354204418195344",
    "acw_sc__v3": "68d4deedd6ed9899700d7191ee988daf4d278e56",
    "ssxmod_itna": "1-QqjODKYvx0hzi7G7bo0=DujbA1Deq0dGMD3Mq7tDRDFqAPDODCOiF8i=WR4AKKdKbmBk5x15BEqDsqqxiNDAg40iDC3mdDn0BGt4Ftma4Qd31mYg04Iomao8yG5AlD1Il80IyZcQGgUU=YiKdfYhs3eIeYGxK4xIiDB3DbqDyKDR24xGGf4GwDGoD34DiDDpfD03Db4D_F1TD7hWa1PFbZjeDQ4GyDitDKLeCxG3D0_WozBDbozRTNDDltGSqGh4oDYPbk1bsdx7DAkGFP_WDjqPD/_5cOKDBFXZqI6aRP3kplmHzxBQD7k7LfbDTKvfFX8TOMrUgNhAd3deMgKbGxoYd5ADOgrs2q_OqO_55A_50qqi4SBhEjdDDfwGbwnpjGEijNVPib=04K45xwgQDyBIgnPKQDzCY4Wh=U21BqGYediG0GRwUAj7x70qYcPPoD",
    "ssxmod_itna2": "1-QqjODKYvx0hzi7G7bo0=DujbA1Deq0dGMD3Mq7tDRDFqAPDODCOiF8i=WR4AKKdKbmBk5x15BP4DW5Oe8uxDLiDD=l_IGH4KDBupmAWwt7DH0eKquQqjEgtYrW7UEKyPMxfpCifdeU5ij777t3mi=H9YQdKT4X9kGE0LjMm_52K027eqIYuud9Gx6NwOjLYuLgGOteBbfkKLjYydFUIw2Dsd3h4MDHqL_AUm3ueeNsH=fX0T=ra/XNTtITkzUX_MToem9NXRP2AR4u_bfAoXFKdNxuzc=7m4Mfy6CZ_qTZjU0qYGdn/f2/EQ0mokEjgmD/=vRaKXr64S_rEI/CYTZYxbXsg_ToU/CXQR3ZY0Aem54Kf0N0YPfebE0GUQ0KgYEQ3O9KWoPCo22DiCKIUntfWugiPsoPiIf16d4lumU5_ZXHcoXeEbcfbZ=DF3d2NjtuvFYy7nE0XO=Ks2IRrQn8FUj=D1tua3_fdaSLYZ36=UVr0o35PBpLGosErhgIVoIh0a003=xt9_a8/LC/LToLAGd52oy0K4w3xZtDS=7GERBN3biV=fbk=n0GdlAYh52ZP2eX5oKCrEh7T3h6jzfjzygpeNlUwmKn0qBCglBdz6pY1oN6W9hP6=N3Qp4BAvsZZm1pHZP0IZlG2iGqlb0Q/gOzKCGie4BNViiP1nwsem_CGG3sVNGiDDNDxD"
}
url = "http://www.ccgp-qinghai.gov.cn/portal/category"
for page in range(1, 5):
    data = {
        "pageNo": page,
        "pageSize": 15,
        "categoryCode": "ZcyAnnouncement1",
        "_t": int(time.time() * 1000)
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data, verify=False).json()



    try:
        for item in response["result"]["data"]["data"]:
            district_name = item.get('districtName', 'N/A')
            title = item.get('title', 'N/A')
            author = item.get('author', 'N/A')
            logger.info(f"地区: {district_name} | 标题: {title} | 发布人: {author}")
    except KeyError as e:
        logger.error(f"响应数据结构异常，缺少键: {e}")
    except Exception as e:
        logger.error(f"处理数据时发生错误: {e}")

