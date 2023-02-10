# _*_ coding: utf-8 _*_
# @Time: 2023/2/10 10:09
# @Author: lemon
# @File: 3.3 pyquery的使用
# @Project: WebCrawlerDevelopment
from pyquery import PyQuery as pq

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


# url初始化
# doc = pq(url='http://cuiqingcai.com')
# print(doc('title'))
# 文件初始化
# doc = pq(filename='path')
# 字符串初始化
doc = pq(html)

# 基本CSS选择器
print('#container .list li')
print(doc('#container .list li'))
print(type(doc('#container .list li')))

# 查找节点
print('查找所有li节点')
lis = doc.find('li')
print(lis)
items = doc('.list')
print('查找ul元素的直接子节点')
lis = items.children()
print(lis)
print('对子节点进一步查找')
lis = items.children('.active')
print(lis)
print('查找直接父节点')
container = items.parent()
print(container)
print('查找符合条件的祖先节点')
parent = items.parents('.wrap')
print(parent)

li = doc('.list .item-0.active')
print('查找兄弟节点')
print(li.siblings('.active'))

# 遍历
print('遍历选择结果')
lis = doc('li').items()
for li in lis:
    print(li, type(li))

# 提取信息
a = doc('.item-0.active a')
print('获取href属性')
print(a.attr('href'))
print(a.attr.href)

a = doc('a')
for item in a.items():
    print(a.attr.href)

print('获取文本')
a = doc('.item-0.active a')
# 结果为多个时，text()方法会将多个节点的所有文本合并成一个字符串返回
print(a.text())
print('获取HTML文本')
li = doc('.item-0.active')
print(li.html())

# 节点操作
print('添加或删除class')
li = doc('.item-0.active')
print(li)
li.remove_class('active')
print(li)
li.add_class('active')
print(li)

print('修改属性')
print(li)
li.attr('name', 'link')
print(li)
li.text('changed item')
print(li)
li.html('<span>changed item</span>')
print(li)

print('移除节点')
# li.remove()

# 伪类选择器
print('获取第一个li')
li = doc('li:first-child')
print(li)
li = doc('li:last-child')
print(li)
li = doc('li:nth-child(2)')
print(li)
# 获取偶数位置的li节点
li = doc('li:nth-child(2n)')
print(li)
li = doc('li:contains(second)')
print(li)
