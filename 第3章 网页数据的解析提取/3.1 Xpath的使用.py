# _*_ coding: utf-8 _*_
# @Time: 2023/2/9 16:32
# @Author: lemon
# @File: Xpath的使用
# @Project: WebCrawlerDevelopment
from lxml import etree

"""
Xpath运算符

运算符	描述	        实　　例	                返　回　值
or	    或	            age=19 or age=20	如果 age 是 19，则返回 true。如果 age 是 21，则返回 false
and	    与	            age>19 and age<21	如果 age 是 20，则返回 true。如果 age 是 18，则返回 false
mod	    计算除法的余数	5 mod 2	            1
                        计算两个节点集	    //book
+	    加法	        6 + 4	            10
-	    减法	        6 - 4	            2
*	    乘法	        6 * 4	            24
div	    除法	        8 div 4	            2
=	    等于	        age=19	            如果 age 是 19，则返回 true。如果 age 是 20，则返回 false
!=	    不等于	        age!=19	            如果 age 是 18，则返回 true。如果 age 是 19，则返回 false
<	    小于	        age<19	            如果 age 是 18，则返回 true。如果 age 是 19，则返回 false
<=	    小于或等于	    age<=19	            如果 age 是 19，则返回 true。如果 age 是 20，则返回 false
>	    大于	        age>19	            如果 age 是 20，则返回 true。如果 age 是 19，则返回 false
>=	    大于或等于	    age>=19	            如果 age 是 19，则返回 true。如果 age 是 18，则返回 false
"""

text = '''
<div>
    <ul>
         <li class="item-0 item" name="item"><a href="link1.html">first item</a></li>
         <li class="li item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''
html = etree.HTML(text)

# 所有节点
res = html.xpath('//li')
print('所有li节点')
print(res)

# 子节点
res = html.xpath('//li/a')
print('所有li节点的所有直接a子节点')
print(res)

res = html.xpath('//ul//a')
print('ul节点下的所有子孙a节点')
print(res)

# 父节点
res = html.xpath('//a[@href="link4.html"]/../@class')
print('href属性为link4.html的a节点的父节点的class属性')
print(res)
res = html.xpath('//a[@href="link4.html"]/parent::*/@class')
print('另一种写法: parent::')
print(res)

# 属性匹配
res = html.xpath('//li[@class="item-0"]')
print('选取class为item-0的li节点')
print(res)

# 文本获取
res = html.xpath('//li[@class="item-0"]/a/text()')
print('获取选取class为item-0的li节点的直接a子节点的文本内容')
print(res)

# 属性获取
res = html.xpath('//li/a/@href')
print('获取所有li节点的直接子节点a的href属性')
print(res)

# 属性多值匹配
res = html.xpath('//li[contains(@class, "li")]')
print('选取class中包含"li"的所有li节点')
print(res)

# 多属性匹配
res = html.xpath('//li[contains(@class, "item") and @name="item"]')
print('选取class中包含item且name为item的所有li节点')
print(res)

# 按序选择
res = html.xpath('//li[1]/a/text()')
# 节点顺序从1开始
print('选取第一个li节点内的文本内容')
print(res)
res = html.xpath('//li[last()]/a/text()')
print('选取最后一个li节点内的文本内容')
print(res)
res = html.xpath('//li[position()<3]/a/text()')
print('选取位置小于3的li节点内的文本内容')
print(res)
res = html.xpath('//li[last()-2]/a/text()')
print('选取倒数第3个li节点的文本内容')
print(res)

# 节点轴选择
res = html.xpath('//li[1]/ancestor::*')
print('选取第一个li节点的所有祖先节点')
print(res)
res = html.xpath('//li[1]/ancestor::div')
print('选取第一个li节点的所有祖先div节点')
print(res)
res = html.xpath('//li[1]/attribute::*')
print('选取第一个li节点的所有属性值')
print(res)
res = html.xpath('//li[1]/child::a[@href="link1.html"]')
print('选取第一个li节点的直接子节点中href属性为link1.html的a节点')
print(res)
res = html.xpath('//li[1]/descendant::span')
print('选取第一个li节点的子孙节点中的span节点')
print(res)
res = html.xpath('//li[1]/following::*[2]/text()')
print('选取第一个li节点的后续节点中的第2个节点的文本内容')
print(res)
res = html.xpath('//li[1]/following-sibling::*')
print('选取第一个li节点的后续兄弟节点')
print(res)
