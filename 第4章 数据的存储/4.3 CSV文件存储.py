# _*_ coding: utf-8 _*_
# @Time: 2023/2/10 11:57
# @Author: lemon
# @File: 4.3 CSV文件存储
# @Project: WebCrawlerDevelopment
import csv
import re

from pyquery import PyQuery as pq

import requests

url = 'https://ssr1.scrape.center/'
html = requests.get(url).text
doc = pq(html)
items = doc('div.el-card')

# 写入
with open('./resource/movie.csv', 'w', encoding='utf-8') as file:
    fields = ['名称', '类别', '上映时间', '评分']
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    for item in items.items():
        name = item.find('h2').text()
        categories = ','.join(item.find('.categories button').text().split(' '))
        publish_time_str = item.find('span:contains(上映)').text()
        publish_time = re.search(r'(\d{4}-\d{2}-\d{2})', publish_time_str).group(1) \
            if publish_time_str and re.search(r'\d{4}-\d{2}-\d{2}', publish_time_str) else None
        score = float(item.find('p.score').text().strip())
        data = {'名称': name, '类别': categories, '上映时间': publish_time, '评分': score}
        writer.writerow(data)

print('保存完成')

# 读取
with open('./resource/movie.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
