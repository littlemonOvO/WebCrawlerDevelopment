# _*_ coding: utf-8 _*_
# @Time: 2023/2/12 11:53
# @Author: lemon
# @File: 7.8 字体反爬实例
# @Project: WebCrawlerDevelopment
import re

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from parsel import Selector

INDEX_URL = 'https://antispider4.scrape.center/page/{page}'
TOTAL_PAGE = 3
TIMEOUT = 10

options = webdriver.ChromeOptions()
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, TIMEOUT)


# 获取并提取class和内容的匹配规则
def get_icon_map():
    css_url = 'https://antispider4.scrape.center/css/app.654ba59e.css'
    resp = requests.get(css_url)
    results = re.findall(r'(icon-\d+):before{content:"(.*?)"}', resp.text, re.S)

    map = {}
    for res in results:
        map[res[0]] = res[1]

    return map


icon_map = get_icon_map()


def scrape_api(url, condition, locator):
    try:
        print(f'scraping {url}...')
        browser.get(url)
        wait.until(condition(locator))
    except TimeoutException:
        print(f'error occurred while scraping url {url}')


def scrape_index(page):
    url = INDEX_URL.format(page=page)
    scrape_api(url, EC.presence_of_all_elements_located, (By.CSS_SELECTOR, 'div.item'))


# 根据class提取真实数据
def get_score(lis):
    score_str = ''
    for item in lis:
        item = re.search(r'(icon-\d+)', item).group(1)
        score_str += icon_map.get(item)
    return float(score_str)


def parse_index():
    sel = Selector(browser.page_source)
    results = []
    for item in sel.css('div.item'):
        name = item.css('h2::text').get()
        categories = ','.join([span.css('::text').get().strip() for span in item.css('.categories button span')])

        # 获取class
        spans = item.css('.score span i::attr(class)').getall()
        score = get_score(spans)

        results.append({
            'name': name,
            'categories': categories,
            'score': score
        })
    return results


def main():
    try:
        for page in range(1, TOTAL_PAGE + 1):
            scrape_index(page)
            print(parse_index())
    finally:
        browser.close()


if __name__ == '__main__':
    main()
