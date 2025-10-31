# -*- coding: utf-8 -*-
"""
Created on 2025-01-08 10:20:59
---------
@summary:
---------
@author: YHLin
"""

import feapder
from feapder import Request

from tb_movie_item import TbMovieItem

import feapder


import feapder

import feapder

class AirDouban(feapder.AirSpider):

    def start_requests(self):
        # 循环生成前10页的请求，使用range从0到250，步长为25
        for start in range(0, 250, 25):
            url = f"https://movie.douban.com/top250?start={start}&filter="
            page_number = (start // 25) + 1
            yield feapder.Request(url, callback=self.parse,page = page_number)

    def parse(self, request, response):
        # 提取每个电影的链接
        movie_urls = response.xpath("/html/body/div[3]/div[1]/div/div[1]/ol/li//div/div[2]/div[1]/a/@href").extract()
        for movie_url in movie_urls:
            print(f"正在爬取电影详情：{movie_url}")
            # 发送请求获取电影的详细信息
            yield feapder.Request(movie_url, callback=self.parse_detail)

    def parse_detail(self,request, response):

        # 提取电影详细信息
        title = response.xpath("//span[@property='v:itemreviewed']/text()").extract_first()
        directors = response.xpath("//a[@rel='v:directedBy']/text()").extract_first()
        country = response.xpath("//div[@id='info']//span[text()='制片国家/地区:']/following-sibling::text()").extract_first()
        summary = response.xpath("//div[@class='related-info']/div[@id='link-report-intra']/span[1]/text()").extract_first()
        rating = response.xpath("//div[@class='rating_self clearfix']/strong[@class='ll rating_num']/text()").extract_first()
        time = response.xpath("//div[@class='subject clearfix']/div[@id='info']/span[14]/text()").extract_first()
        release_date = response.xpath("//div[@class='subject clearfix']/div[@id='info']/span[11]/text()").extract_first()

        # 输出提取的信息
        print("电影：{} 导演：{} 地区：{} 简介：{} 评分：{} 片长：{} 上映时间：{} ".format(title, directors, country,summary,rating, time,release_date))
        item = TbMovieItem()
        item.title = title
        item.directors = directors
        item.country = country
        item.summary = summary
        item.rating = rating
        item.time = time
        item.release_date = release_date

        yield item


    def download_midware(self, request: Request):
        request.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://cn.bing.com/",
            "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "cross-site",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
        }
        request.cookies = {
            "ll": "\"118323\"",
            "bid": "DqV2HJCNRKg",
            "_pk_id.100001.4cf6": "7f9615e8cedc3596.1734154335.",
            "_vwo_uuid_v2": "D78F451AB9E92E573CF821847EDB1B302|6e79cb8ad4cc1b6a1ce06b92ad06cc09",
            "__yadk_uid": "06hrgW4zgK9TY6BlsbKAe01W2k1OYppv",
            "dbcl2": "\"285826509:hfvCzim70Ms\"",
            "push_noty_num": "0",
            "push_doumail_num": "0",
            "__utmv": "30149280.28582",
            "ck": "y_9I",
            "_pk_ref.100001.4cf6": "%5B%22%22%2C%22%22%2C1736303691%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D",
            "_pk_ses.100001.4cf6": "1",
            "ap_v": "0,6.0",
            "__utma": "223695111.795355384.1734154335.1736255068.1736303691.6",
            "__utmb": "223695111.0.10.1736303691",
            "__utmc": "223695111",
            "__utmz": "223695111.1736303691.6.5.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/"
        }
        return request


if __name__ == "__main__":
    AirDouban().start()