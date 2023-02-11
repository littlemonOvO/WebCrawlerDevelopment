# _*_ coding: utf-8 _*_
# @Time: 2023/2/10 11:31
# @Author: lemon
# @File: 4.2 JSON文件存储
# @Project: WebCrawlerDevelopment
import json

import requests
from parsel import Selector

url = 'https://ssr1.scrape.center/'
html = requests.get(url).text
selector = Selector(text=html)
items = selector.css('div.el-card')

with open('./resource/movie.json', 'w', encoding='utf-8') as file:
    datas = []
    for item in items:
        name = item.css('h2::text').get()
        categories = ','.join(item.css('div.categories button span::text').getall())
        publish_time = item.xpath('.//span[contains(text(), "上映")]/text()').re_first(r'\d{4}-\d{2}-\d{2}')
        score = item.xpath('//p[contains(@class, "score")]/text()').get()
        data = {
            'name': name,
            'categories': categories,
            'publish_time': publish_time,
            'score': float(score)
        }
        datas.append(data)
    # ensure_ascii=False确保可输出中文, indent为缩进字符数
    file.write(json.dumps(datas, indent=2, ensure_ascii=False))

print('保存完成')

