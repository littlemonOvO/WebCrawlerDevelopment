# _*_ coding: utf-8 _*_
# @Time: 2023/2/10 10:39
# @Author: lemon
# @File: 3.4 parsel的使用
# @Project: WebCrawlerDevelopment
from parsel import Selector

html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
'''

selector = Selector(text=html)
# css
items = selector.css('.item-0')
print(items)
# xpath
items = selector.xpath('//li[contains(@class, "item-0")]')
print(items)

# 提取文本
items = selector.css('.item-0')
for item in items:
    text = item.xpath('.//text()').get()
    print(text)

items = selector.xpath('//*[contains(@class, "item-0")]')
for item in items:
    text = item.css('::text').get()
    print(text)

# 提取属性
res = selector.css('.item-0.active a::attr(href)').get()
print(res)
res = selector.xpath('//li[contains(@class, "item-0") and contains(@class, "active")]/a/@href').get()
print(res)

# 正则提取
res = selector.css('.item-0').re('link.*')
print(res)
res = selector.css('.item-0 *::text').re('.*item')
print(res)
res = selector.css('.item-0').re_first('<span class="bold">(.*?)</span>')
print(res)
