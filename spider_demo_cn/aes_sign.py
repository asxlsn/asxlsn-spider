import requests


headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.spiderdemo.cn/authentication/symmetry_challenge/?challenge_type=symmetry_challenge",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "x-aes-token": "zvICIrpWOcQ69ttsU8wU5WzMaEY06jRbl1r7st7mEApOVw==",
    "x-des-token": "EPKvpCl4aSx0+g9tThm65+2a9vIvoqJHUQLKBJLfdqvcrJ0YtNdmtA=="
}
cookies = {
    "sessionid": "rlh8qae06qiyhpurbdadielyav3yptw7"
}
url = "https://www.spiderdemo.cn/authentication/api/symmetry_challenge/page/2/"
params = {
    "challenge_type": "symmetry_challenge",
    "aes_sign": "+WSkBuYfTT5lH37rJl9qpeN9ZqcuSC4cEOk9djfT5sheSw==",
    "des_sign": "EPKvpCl4aSx0+g9tThm65+2a9vIvoqJHUQLKBJLfdqutL9NTF8WydBrbDSuriEII",
    "t": "1760154270577"
}
response = requests.get(url, headers=headers, cookies=cookies, params=params)

print(response.text)
print(response)