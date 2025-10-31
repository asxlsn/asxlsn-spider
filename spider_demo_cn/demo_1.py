import asyncio
import httpx

headers = {
    "Host": "www.spiderdemo.cn",
    "Connection": "keep-alive",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.spiderdemo.cn/sec1/header_check/",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cookie": "sessionid=rlh8qae06qiyhpurbdadielyav3yptw7"
}


async def fetch_page(client, i):
    url = f"https://www.spiderdemo.cn/sec1/api/challenge/page/{i}/?challenge_type=header_check"
    try:
        response = await client.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        total_page = sum(data.get("page_data", []))
        print(f"第 {i} 页成功，值为 {total_page}")
        return total_page
    except Exception as e:
        print(f"第 {i} 页请求失败：{e}")
        return 0


async def main():
    total = 0
    async with httpx.AsyncClient(headers=headers, http2=True) as client:
        # 限制并发数量（防止被封）
        sem = asyncio.Semaphore(10)

        async def sem_fetch(i):
            async with sem:
                return await fetch_page(client, i)

        tasks = [asyncio.create_task(sem_fetch(i)) for i in range(1, 101)]
        results = await asyncio.gather(*tasks)
        total = sum(results)
        print(f"\n✅ 100 页的和为：{total}")


if __name__ == "__main__":
    asyncio.run(main())




