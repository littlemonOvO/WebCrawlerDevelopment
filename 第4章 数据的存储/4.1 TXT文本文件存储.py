# _*_ coding: utf-8 _*_
# @Time: 2023/2/10 11:11
# @Author: lemon
# @File: 4.1 TXT文本文件存储
# @Project: WebCrawlerDevelopment
import requests
from pyquery import PyQuery as pq
import re

"""
优点: TXT文本操作简单，几乎兼容任何平台
缺点：不利于检索
"""

url = 'https://ssr1.scrape.center/'
html = requests.get(url).text
doc = pq(html)
items = doc('div.el-card')

with open('./resource/movie.txt', 'w', encoding='utf-8') as file:
    for item in items.items():
        name = item.find('h2').text()
        categories = ','.join(item.find('.categories button').text().split(' '))
        public_time_str = item.find('span:contains(上映)').text()
        public_time = re.search(r'(\d{4}-\d{2}-\d{2})', public_time_str).group(1) \
            if public_time_str and re.search(r'\d{4}-\d{2}-\d{2}', public_time_str) else None
        score = item.find('p.score').text().strip()
        file.write(f'名称: {name}\n')
        file.write(f'类别: {categories}\n')
        file.write(f'上映时间: {public_time}\n')
        file.write(f'评分: {score}\n')
        file.write('-' * 50 + '\n')
print('保存完成')
