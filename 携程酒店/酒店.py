from pprint import pprint

import requests
import json



headers = {
    "authority": "m.ctrip.com",
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/json",
    "duid": "u=3EA5D07A8DFD819CB860B2FFE37CCEB4&v=0",
    "phantom-token": "1004-minicommon-U2FsdGVkX19KLS81m2o17q2bFA+AAthQYDRYaGPDkzfKCp4elJ7u+NJFgITmNo/zVwHecO+dSwKjZCzLoT6ksziSJihvlP5B9luImk3vAeMV51RgtLfP9JnewMO4VdPCTKXnnKOmQl1lkiR2HJYw0vIAmY0dC37OLuciYHxuyLwyfbzlNgga9i0O9rxdjcAPFvv425Gqb7rg997kZBj8rO6qQt3w0oOIiFPNMsSXjjM9vXRNNUBP0QfeQ73XechDPaNtwvC5FHQUJocK2VoArerU2X9oXNHq8ybB1YRczHp9IPmcNCyDkeRzLRUxycr7JTLnHyBUXrVbLHegNr56tY35tQBiRpas54YKkhlGAsYk6Rwt5dBY8DJwlHe7Yt6JnqESs+2ZHENxGZKe9RJ0yc1K6C/0WaNtoNvyRI4H0Derbf6GhNEj5t81xZzGmjTIADa+WUkDoBcxVr3dGVzT36FzdU1DOk/cQLvqf89GpLMI4Lgim+wYcF1BnJy6Q3go+shBkp473QqFm3hKRU+p1b2FD0ZYuSX0jgPay0w4B/mmnXXT4rnMO8VEkS0a46Fvite6GaeEDPyInaCYQvptgHBVu6efCd7LDCbck+sxav1O7XT0AnVn3gcw9NCThgbjiFFTapFc+YK3ttdKe2zf4Td0DnTacYvg5mtlxf3qJy+tuMQUP0GEGcZlA5S0m6TAsU0AuFTOwlzkfKxkFOMyWOq3xZJaKXscB0cQnwihktQyNlBOfw6kW66gDAxOTI3tJ5xDrOYgN51SbNUbjSBZ6U51usqd5tJi+sbFax62i3epnflhDKZEu4h/b1DJj+F3wGdFsiT7WGolqg6HF4QHv5m+j14DjyrxREOPCoM3IMt/2SjAhOcj7zmXx5KNIi1Ix2COnqOdBc5qLbI4mBYWl491MZ7tTcRrxEr+bWRb41m3VgPnewvY4fmCFqzr1whlwYCUSw9pq+fTri2300BlJXkLB9EOauzgtqi9gyzYQ9TWUuQbyJSxv6q4v5BcsF+zX6Dbk+kxJhnqexYJd60Tyg==",
    "referer": "https://servicewechat.com/wx0e6ed4f51db9d078/1006/page-frame.html",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "udl": "708D70C2B179E2F91CC5ED1C2CCE362D",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
    "x-ctx-currency": "CNY",
    "x-ctx-group": "ctrip",
    "x-ctx-locale": "zh-CN",
    "x-ctx-personal-recommend": "1",
    "x-ctx-region": "CN",
    "x-ctx-ubt-pageid": "10650138110",
    "x-ctx-ubt-pvid": "19",
    "x-ctx-ubt-sid": "1",
    "x-ctx-ubt-vid": "1756074758919.b9a6LVVuw3DZ",
    "x-wx-include-credentials": "env",
    "x-wx-openid": "f3e6cbec-2c3b-4ccf-8a63-27f7debbe3e4",
    "xweb_xhr": "1"
}
cookies = {
    "Union": "OUID=&AllianceID=262684&SID=711465&SourceID=55552689",
    "DUID": "u=3EA5D07A8DFD819CB860B2FFE37CCEB4&v=0",
    "_udl": "708D70C2B179E2F91CC5ED1C2CCE362D",
    "GUID": "52271076296566298890"
}
url = "https://m.ctrip.com/restapi/soa2/31454/gethotellist"
params = {
    "_fxpcqlniredt": "52271076296566298890"
}
for page_index in range(1, 6):
    print(f"第页{page_index}数据")
    data = {
        "head": {
            "cid": "52271076296566298890",
            "ctok": "",
            "cver": "999999",
            "lang": "01",
            "sid": "",
            "syscode": "30",
            "auth": "BFA4523BAF43B66C4EE9C8C0EA3591CE7D99E395E2E3F3D930910436F199AA8E",
            "sauth": "",
            "platform": "Applet",
            "aid": "",
            "ouid": "",
            "locale": "zh-CN",
            "pageId": "10650138110",
            "currency": "CNY",
            "timezone": "8",
            "isSSR": False,
            "group": "ctrip",
            "bu": "HBU",
            "extension": [
                {
                    "name": "appId",
                    "value": "wx0e6ed4f51db9d078"
                },
                {
                    "name": "scene",
                    "value": "1256"
                }
            ]
        },
        "paging": {
            "pageCode": "",
            "pageIndex": page_index,
            "pageSize": 10
        },
        "searchType": 2,
        "mapType": 2,
        "hotelIdFilter": {
            "hotelIds": [],
            "pinnedHotelIds": [
                0
            ],
            "hiddenHotelIds": [],
            "preHotelIds": []
        },
        "location": {
            "countryId": 1,
            "provinceId": 0,
            "districtId": 0,
            "cityId": 28,
            "region": "",
            "isOversea": False
        },
        "coordinates": [
            {
                "type": 2,
                "cityID": 28,
                "latitude": "30.656179428100586",
                "longitude": "104.08329010009766"
            }
        ],
        "filterTags": {},
        "orderingByUser": False,
        "date": {
            "checkInDate": "2025-08-25",
            "checkOutDate": "2025-08-26"
        },
        "customerFilter": {
            "roomCount": 1
        },
        "queryType": "NORMAL",
        "extendableParams": {
            "sessionId": ""
        },
        "filters": [
            {
                "filterID": "29|1",
                "type": "29",
                "title": "1成人,0儿童",
                "value": "1|1"
            },
            {
                "filterID": "17|1",
                "type": "17",
                "value": "1",
                "subType": "2"
            }
        ],
        "guestFilter": [
            {
                "filterID": "29|1",
                "type": "29",
                "title": "1成人,0儿童",
                "value": "1|1"
            }
        ]
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)

    hotel_list = response.json()["data"]["hotelList"]
    for hotel in hotel_list:
        print(hotel)
