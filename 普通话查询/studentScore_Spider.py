import requests
from govVerifyImage_Spider import get_verify_code

def get_student_score(name, stu_id, id_card, uid):
    """
    获取学生成绩信息
    每次请求都使用新的验证码
    """
    # 每次请求前获取新的验证码
    verify_code = get_verify_code()
    print(f"当前验证码为: {verify_code}")

    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://zwfw.moe.gov.cn",
        "Pragma": "no-cache",
        "Referer": "https://zwfw.moe.gov.cn/mandarin/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "pm": "name,stuId,idCard,uid,verifyCode",
        "reqType": "3",
        "rn": "1760450916263",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sign": "10d1a4251b65143e205035b8b8eb3fac",
        "uid;": ""
    }

    cookies = {
        "_abfpc": "e04de75d72ef947532f3c7ed97eb967560e42291_2.0",
        "cna": "1a9e2a47231636ffc1133d4c115c32f8"
    }

    url = "https://zwfw.moe.gov.cn/eduSearch/prod/moe/verify/studentScore"

    # 使用新获取的验证码
    data = {
        "name": name,
        "stuId": stu_id,
        "idCard": id_card,
        "uid": uid,
        "verifyCode": verify_code  # 使用动态获取的新验证码
    }

    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    return response

# 调用函数获取成绩
response = get_student_score(
    name="杨慧明",
    stu_id="510412025840148",
    id_card="513721200109290187",
    uid="1978100601459691522"
)

print(response.text)

