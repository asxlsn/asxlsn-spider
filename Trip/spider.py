from pprint import pprint

import requests
import json


headers = {
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "currency": "HKD",
    "locale": "zh-HK",
    "origin": "https://hk.trip.com",
    "p": "46646959714",
    "phantom-token": "1004-common-ZQgva7rQAy48r1Dr3Bj9hwQMY1DeA7YlbjUDJPTE4zvacyBqid0EtLRtsvohEGQyq5j3Hyfgy1kELMJT9E6Xi5Fw7zrqAw6LxP4wdgw5my7UY6tYfFxpYnLITEOnKaSR3DyNkJkNjpUv4mwsQj7HJHAyPmwFsW60RdPjXkv5vDMWPYbBEtmRcPwc7KntjLcjT5El8ynEMfiOkY3EqMYUlyZE7zYUSytaKMSrOpIsUjtLwPqeHsEhFIZBwn9i3ZRDEqNY5AyqNKhci0oj67jdtWsAyDE0bYPQyAlWHMeqfy8lj0Egpi0byh5waPeXHj9tIhEGPiM5J0nJk8j8EqOYHdwtUwH6e4tj6pI7DWZ7EqUR4cjnEN7iZbJ7EocYSBJL3w4TvBE5fYBmJ7hYZLwdEP6Y0QJDnvaGvAE6GY56JtZwl3wmEszY6oJLgitHjHEB9YLlJZQYp3yME7UYDQwLGEFtwXdiqzxBLeFZYPBwTajhQxU7yPES7i3SJg9W1EF4YShwZ5wOqi0Bvs4YTpj80wmbItGxdfygEqXiH8JDSRBEOQYlFwzAygde7QysGjSaw3leHSwf6jTMxq3yQEOmiPBJpAWlEFSYfPw16whpKUFj5LwqUrcGeskY9EUci7TJPFY9BWLOYmlJzEUHY30JZgYnoy5bWh0vXESoYo4JSsYmhyPqYDcyXE4tYz0wk3w8QKhGjd6wp9rk4i3AvsDjcEUTigZJN5YnNWGFYNSJDEOsYn1J6ZYnly1cWBDvQEbtY4NJUlYL3yHqYcBjBE4SYNOwscJnZE1AwHnEamvgZwctw8Ep9ikUJtGvo0e7bJhE5kYl5wdswAowkDY0EB6i9dJaZRpEAGY16whOEq8yPnvABWNPjqEBPiczJS8YsEsOYHMwzNwBHKd0ethW3hySbwFAjs1YoE1Si0AJnfWLEhOYHDw89ygajqnEkaw7OwGTK3HicBizdeQ3YUDjf3wTNEgYZPj5XiSpwTsRmFyH8J1bEFoynkR3qjZdvObJ96wS9w3fW0Qjl0In1jMAvtkEP3vkMJ98jdSeOTEgLy06ySpRfpiHtITMRHMjUYA4eLFYODe3ARl5idzW1FRG6EfAWshil5JSNeonjTny63wBLwFPeTzEN4RsGwBzwkQedGjbUE8lyDkJB4e37wAPRosJ46wplvtHEQbYkAWDavSUWldRdpyoZiojoSikYUNEHniT6jf3Y8TEc8Y8aw60j1SycaYhQw1PrQMR56x9YOHWaqY8SymUYTXEpUe3Pxd9w4YqUIXmxfwbtvNzegbYmLiGQYbcE0Bx7PKGYN4vUUKPBj9TeSoEh0j9OWPyL4rhyDYfAIFOJ19WpBr5aKp4eg6EOPWXoR4ORQAIDYG8J1LvB0Ko1R0QJqAisBwcOesOjQ8wLsEBMWnpjLZJNYNTxFQrz6yAlRbqJU1iQhwkpeU5jX9Y8DEaNxzEOZi9YHpWmNe9kW1niSpwHZJQbxGXinLemYs1WPUKlnyNcY4Xif6wDZRAfEs9W10xtTeonEBY7tJ44x8DetTJqcYqoxT8ekYM9yDkIfXwTFjs1whQvUZjosvctrPPKUYk1yszJPBx79YHkiNoIgMvGYGgKZ9rPpytNjsMwokvAtj9NrBZvTfiHYT4rL8vsFYaAJQbW7cYtBYNyoY5UeP0x06I1UjkAi6Xi1GxMZW6bjBrf5x4SYlLwmcIkr7ybBWOcjM7x51JbTxMHYmjDGjgUxLJGYDfELdJngY0ORXfWnqiT1Y3zWFDwkqwOpjS9RHLEhdjOSESQKkG",
    "pid": "c3fc0bf0-dd47-4b5a-b035-e923533d05f6",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://hk.trip.com/hotels/list?city=58&cityName=%E9%A6%99%E6%B8%AF&provinceId=0&countryId=1&districtId=0&checkin=2025%2F09%2F27&checkout=2025%2F09%2F28&barCurr=HKD&crn=1&adult=2&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=true&listFilters=29~1*29*1~2*2%2C17~1*17*1*2%2C80~0~1*80*0*2&locale=zh-HK&curr=HKD",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "trip-trace-id": "1754718956608.8fafqtKaFU13-1758968576051-1458948941",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "x-traceid": "1754718956608.8fafqtKaFU13-1758968576051-1458948941"
}
cookies = {
    "UBT_VID": "1754718956608.8fafqtKaFU13",
    "ibu_online_jump_site_result": "{\"site_url\":[\"hk.trip.com\"],\"suggestion\":[]}",
    "ibu_online_home_language_match": "{\"isRedirect\":false,\"isShowSuggestion\":true,\"lastVisited\":true,\"region\":\"cn\",\"redirectSymbol\":false}",
    "_abtest_userid": "d0e5ea17-2668-4882-8d04-e22e1ec688a7",
    "GUID": "09034046114121872208",
    "_gcl_gs": "2.1.k1$i1754718955$u30159398",
    "_gcl_au": "1.1.260303671.1754718961",
    "_ga": "GA1.1.861124272.1754718961",
    "_fwb": "78asaAegwn1s2L5CQzLyEf.1754718960610",
    "_RF1": "240e%3A39c%3Ad7%3A88a0%3Af4a9%3A4872%3A6479%3A2ac1",
    "_RSG": "L_KVMR6EdnDUifY6JtfB5A",
    "_RDG": "28b3278db322b825f0313747c3df6d5539",
    "_RGUID": "dc673866-d67d-4fd5-a14b-a774c68a9b1e",
    "_tt_enable_cookie": "1",
    "_ttp": "01K26PCZ19QFP8TD0JW7GX9WDN_.tt.1",
    "_ym_uid": "1754718961174996537",
    "_ym_d": "1754718961",
    "_gcl_aw": "GCL.1754719008.CjwKCAjwwNbEBhBpEiwAFYLtGDGk8qwgv-pIlWsHMQ3y4UAZPLpmDd70DCK5oouBKPR6m3MccGRC_BoCnngQAvD_BwE",
    "_scid": "UOREVuM1w3kJAQyquxz8F1X5ANZ92lEv",
    "_fbp": "fb.1.1754719036980.192406319115918757",
    "_scid_r": "WWREVuM1w3kJAQyquxz8F1X5ANZ92lEvdgQJVg",
    "wcs_bt": "s_33fb334966e9:1754719208",
    "_uetvid": "8714d47074e511f0991285063e5e1787",
    "ttcsid": "1754718960687::Zoa3pcMcMoHRycwf-30s.1.1754719210288",
    "ttcsid_CIR4RVBC77UD5V58BBNG": "1754718960687::MmLXUNoxop-fppZG4bYy.1.1754719210527",
    "ttcsid_D1D20OJC77U6QKGC2U2G": "1754718960688::fszNZ5uROXAFKGSnf6gx.1.1754719210527",
    "ttcsid_D1D23DRC77U546UPTDOG": "1754718960688::dHwGXuRXlr56-h-VmqrV.1.1754719210527",
    "_ga_X437DZ73MR": "GS2.1.s1754718960$o1$g1$t1754719289$j60$l0$h0",
    "ibulanguage": "HK",
    "ibulocale": "zh_hk",
    "cookiePricesDisplayed": "HKD",
    "ibu_country": "HK",
    "ibu_cookie_strict": "0",
    "devicePixelRatio": "1.25",
    "g_state": "{\"i_l\":0}",
    "cticket": "BC070849F49DE7B542B33F1EE8A7674AA247E7583B3E33C1D341D73BFFB67E81",
    "login_type": "0",
    "DUID": "u=1E879A8651C1D084777A839131D6C777DD326BDF5E490B5584FF350B64DBD95C&v=0",
    "IsNonUser": "F",
    "ibu_h5_isquick": "0",
    "_udl": "B65C4933EEDF6B5BDE1A8622319894C3",
    "login_uid": "\"\"",
    "ibu_hotel_search_date": "%7B%22checkIn%22%3A%222025%2F09%2F27%22%2C%22checkOut%22%3A%222025%2F09%2F28%22%7D",
    "ibu_online_permission_cls_ct": "2",
    "ibu_online_permission_cls_gap": "1758964305460",
    "IBU_TRANCE_LOG_P": "46646959714",
    "ibu_hotel_search_target": "%7B%22countryId%22%3A1%2C%22provinceId%22%3A0%2C%22searchWord%22%3A%22%22%2C%22cityId%22%3A58%2C%22searchType%22%3A%22%22%7D",
    "oldLocale": "zh-HK",
    "ibu_hotel_search_recent_filter": "%5B%7B%22filterId%22%3A%2275%7CTAG_495%22%2C%22value%22%3A%22495%22%7D%5D",
    "ibusite": "HK",
    "ibugroup": "trip",
    "ibu_hotel_search_crn_guest": "%7B%22adult%22%3A%222%22%2C%22children%22%3A%220%22%2C%22ages%22%3A%22%22%2C%22crn%22%3A%221%22%7D",
    "_bfa": "1.1754718956608.8fafqtKaFU13.1.1758968487976.1758968506408.3.3.10320668148",
    "IBU_showtotalamt": "0"
}
url = "https://hk.trip.com/htls/getHotelList"
params = {
    "x-traceID": "1754718956608.8fafqtKaFU13-1758968576051-1458948941"
}
data = {
    "guideLogin": "T",
    "search": {
        "sessionId": "350c734c-5438-470b-4558-6b643c1bae76",
        "preHotelCount": 12,
        "preHotelIds": [
            344975,
            436847,
            120038931,
            436835,
            436834,
            130238078,
            426551,
            425085,
            344957,
            428254,
            344946,
            344920
        ],
        "checkIn": "20250927",
        "checkOut": "20250928",
        "sourceFromTag": "",
        "filters": [
            {
                "filterId": "29|1",
                "type": "29",
                "value": "1|2",
                "subType": "2"
            },
            {
                "filterId": "17|1",
                "type": "17",
                "value": "1",
                "subType": "2"
            },
            {
                "filterId": "80|0|1",
                "type": "80",
                "value": "0",
                "subType": "2"
            }
        ],
        "pageCode": 10320668148,
        "location": {
            "geo": {
                "countryID": 1,
                "provinceID": 0,
                "cityID": 58,
                "districtID": 0,
                "oversea": False
            },
            "coordinates": []
        },
        "pageIndex": 2,
        "pageSize": 10,
        "needTagMerge": "T",
        "roomQuantity": 1,
        "orderFieldSelectedByUser": False,
        "hotelId": 0,
        "hotelIds": [],
        "lat": 22.301347066368034,
        "lng": 114.1832324183525,
        "tripWalkDriveSwitch": "T",
        "resultType": "",
        "nearbyHotHotel": {},
        "recommendTimes": 0,
        "crossPromotionId": "",
        "travellingForWork": False
    },
    "batchRefresh": {
        "batchId": "",
        "batchSeqNo": 0
    },
    "queryTag": "NORMAL",
    "mapType": "MAPBOX",
    "extends": {
        "crossPriceConsistencyLog": "",
        "NewTaxDescForAmountshowtype0": "B",
        "TaxDescForAmountshowtype2": "T",
        "MealTagDependOnMealType": "T",
        "MultiMainHotelPics": "T",
        "enableDynamicRefresh": "T",
        "isFirstDynamicRefresh": "T",
        "ExposeBedInfos": "F",
        "TaxDescRemoveRoomNight": "",
        "priceMaskLoginTip": "",
        "NeedHotelHighLight": "T",
        "NeedNewHighLightModule": "",
        "NeedBanCommentTag": "",
        "needEntireSetRoomDesc": ""
    },
    "head": {
        "platform": "PC",
        "clientId": "1754718956608.8fafqtKaFU13",
        "bu": "ibu",
        "group": "TRIP",
        "aid": "",
        "sid": "",
        "ouid": "",
        "caid": "",
        "csid": "",
        "couid": "",
        "region": "HK",
        "locale": "zh-HK",
        "timeZone": "8",
        "currency": "HKD",
        "p": "46646959714",
        "pageID": "10320668148",
        "deviceID": "PC",
        "clientVersion": "0",
        "frontend": {
            "vid": "1754718956608.8fafqtKaFU13",
            "sessionID": "3",
            "pvid": "3"
        },
        "extension": [
            {
                "name": "cityId",
                "value": "58"
            },
            {
                "name": "checkIn",
                "value": "2025/09/27"
            },
            {
                "name": "checkOut",
                "value": "2025/09/28"
            },
            {
                "name": "region",
                "value": "HK"
            }
        ],
        "tripSub1": "",
        "qid": 555867529772,
        "pid": "c3fc0bf0-dd47-4b5a-b035-e923533d05f6",
        "hotelExtension": {},
        "cid": "1754718956608.8fafqtKaFU13",
        "traceLogID": "4a9bcf8bb7c76",
        "ticket": "",
        "href": "https://hk.trip.com/hotels/list?city=58&cityName=%E9%A6%99%E6%B8%AF&provinceId=0&countryId=1&districtId=0&checkin=2025%2F09%2F27&checkout=2025%2F09%2F28&barCurr=HKD&crn=1&adult=2&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=true&listFilters=29~1*29*1~2*2%2C17~1*17*1*2%2C80~0~1*80*0*2&locale=zh-HK&curr=HKD",
        "deviceConfig": "M"
    }
}
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)

pprint(response.text)
