# _*_ coding: utf-8 _*_
# @Time: 2023/2/11 17:50
# @Author: lemon
# @File: 7.5 Selenium爬取实战
# @Project: WebCrawlerDevelopment
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from urllib.parse import urljoin
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = 'https://spa2.scrape.center/page/{page}'
TIMEOUT = 10
TOTAL_PAGE = 10

browser = webdriver.Chrome()
wait = WebDriverWait(browser, timeout=TIMEOUT)


# 通用爬取接口
def scrape_api(url, condition, locator):
    logging.info(f'scraping {url}...')
    try:
        browser.get(url)
        wait.until(condition(locator))
    except TimeoutException:
        logging.error(f'error occurred while scraping {url}.', exc_info=True)


# 列表页爬取接口
def scrape_index(page):
    url = INDEX_URL.format(page=page)
    scrape_api(url, EC.visibility_of_all_elements_located, (By.CSS_SELECTOR, 'div.el-card'))


# 列表页解析接口
def parse_index():
    elements = browser.find_elements(By.CSS_SELECTOR, 'div.el-card a[class="name"]')
    return [urljoin(browser.current_url, element.get_attribute('href')) for element in elements]


# 详情页爬取接口
def scrape_detail(url):
    scrape_api(url, EC.visibility_of_all_elements_located, (By.CSS_SELECTOR, 'div.item'))


# 详情页解析接口
def parse_detail():
    name = browser.find_element(By.CSS_SELECTOR, '.item h2').text
    categories = [element.text for element in browser.find_elements(By.CSS_SELECTOR, '.item .categories button span')]
    url = browser.current_url
    cover = browser.find_element(By.CSS_SELECTOR, '.item img').get_attribute('src')
    score = browser.find_element(By.CSS_SELECTOR, '.item .score').text
    drama = browser.find_element(By.CSS_SELECTOR, '.item .drama p').text
    return {
        'url': url,
        'categories': categories,
        'name': name,
        'cover': cover,
        'score': float(score),
        'drama': drama
    }


# 入口
def main():
    try:
        for page in range(1, TOTAL_PAGE + 1):
            scrape_index(page)
            detail_urls = parse_index()
            for detail_url in detail_urls:
                scrape_detail(detail_url)
                data = parse_detail()
                logging.info(f'detail data: {data}')
    finally:
        browser.close()


if __name__ == '__main__':
    main()
