# _*_ coding: utf-8 _*_
# @Time: 2023/2/10 9:12
# @Author: lemon
# @File: 3.2 Beautiful Soup的使用
# @Project: WebCrawlerDevelopment
import re

from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

soup = BeautifulSoup(html, 'lxml')
print(soup.prettify())
print('=' * 40)

# 节点选择器
print(soup.title)
print(soup.head)
# 只选择第一个匹配节点
print(soup.p)

# 提取信息
print('提取文本')
print(soup.title.string)
print('获取名称')
print(soup.title.name)
# 获取属性
print('获取所有属性')
print(soup.p.attrs)
print('获取指定属性值')
print(soup.p['name'])
print('获取class,可能为多个值,返回值为列表')
print(soup.p['class'])

# 嵌套选择
print(soup.head.title.string)

html = """
<html>
    <head>
        <title>The Dormouse's story</title>
    </head>
    <body>
        <p class="story">
            Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1">
                <span>Elsie</span>
            </a>
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> 
            and
            <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
            and they lived at the bottom of a well.
        </p>
        <p class="story">...</p>
"""
soup = BeautifulSoup(html, 'lxml')

# 关联选择
# 子节点和子孙节点
print('4获取直接子节点,返回列表类型')
print(soup.p.contents)
print('获取直接子节点,返回生成器类型')
for i, child in enumerate(soup.p.children):
    print(child)
print('获取子孙节点')
for i, child in enumerate(soup.p.descendants):
    print(child)
print('获取父节点')
print(soup.a.parent)
print('获取所有祖先节点')
print(list(soup.a.parents))
print('获取兄弟节点')
print('获取下一个兄弟节点')
print(soup.a.next_sibling)
print('获取上一个兄弟节点')
print(soup.a.previous_sibling)
print('获取之后的兄弟节点')
print(list(soup.a.next_siblings))
print('获取之前的兄弟节点')
print(list(soup.a.previous_siblings))

html = '''
<div class="panel">
    <div class="panel-heading">
        <h4>Hello, this is a link</h4>
    </div>
    <div class="panel-body">
        <ul class="list" id="list-1" name="elements">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
            <li class="element">Jay</li>
        </ul>
        <ul class="list list-small" id="list-2">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
        </ul>
    </div>
</div>
'''
soup = BeautifulSoup(html, 'lxml')

# 方法选择器
# find()/find_all() 查询所有/单个符合条件的元素
print('获取所有ul节点')
print(soup.find_all(name='ul'))
print('获取所有ul节点内的li节点的文本内容')
for ul in soup.find_all(name='ul'):
    for li in ul.find_all(name='li'):
        print(li.string)

print('获取所有id为list-1的元素')
print(soup.find_all(attrs={'id': 'list-1'}))
print('获取name为elements的元素')
print(soup.find(attrs={'name': 'elements'}))
print('获取所有class为element的元素')
print(soup.find_all(class_='element'))

print('获取带有link的文本信息')
print(soup.find_all(string=re.compile('link')))
print(soup.find_all(string='Hello, this is a link'))


html='''
<div class="panel">
    <div class="panel-heading">
        <h4>Hello</h4>
    </div>
    <div class="panel-body">
        <ul class="list" id="list-1">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
            <li class="element">Jay</li>
        </ul>
        <ul class="list list-small" id="list-2">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
        </ul>
    </div>
</div>
'''
soup = BeautifulSoup(html, 'lxml')
# CSS选择器
print('css selector: .list li')
print(soup.select('.list li'))
for ul in soup.select('.list'):
    for li in ul.select('li'):
        print(li.string)

# 获取属性
for ul in soup.select('ul'):
    print(ul['id'])
    print(ul.attrs['id'])
    