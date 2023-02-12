# _*_ coding: utf-8 _*_
# @Time: 2023/2/12 10:55
# @Author: lemon
# @File: 7.7 CSS位置偏移反爬实例
# @Project: WebCrawlerDevelopment
import asyncio
import logging
import re

from pyppeteer import launch
from pyppeteer.errors import TimeoutError

from parsel import Selector

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = 'https://antispider3.scrape.center/page/{page}'
TOTAL_PAGE = 10


async def init():
    browser = await launch(args=['--disable-infobars'])
    tab = await browser.newPage()
    return browser, tab


async def scrape_api(url, tab, selector):
    logging.info(f'scraping {url}...')
    try:
        await tab.goto(url)
        await tab.waitForSelector(selector)
    except TimeoutError:
        logging.error(f'error occurred while scraping {url}', exc_info=True)


async def scrape_index(page, tab):
    url = INDEX_URL.format(page=page)
    await scrape_api(url, tab, 'div.item')


async def parse_index(tab):
    return await tab.querySelectorAllEval('.item .top a', 'nodes => nodes.map(node => node.href)')


async def scrape_detail(url, tab):
    await scrape_api(url, tab, 'div.item')


# 解析css偏移，还原数据
def parse_detail_data(html):
    sel = Selector(html)

    # 解析名称
    # 存在css偏移
    if sel.css('h2.name span'):
        li = []
        for span in sel.css('h2.name span'):
            offset = int(re.search(r'(\d+)', span.css('::attr(style)').get()).group(1))
            text = span.css('::text').get().strip()
            li.append((offset, text))
        li.sort(key=lambda x: x[0])
        name = ''.join([item[1] for item in li])
    # 不存在css偏移
    else:
        name = sel.css('h2.name::text').get()

    return {
        'name': name
    }


async def parse_detail(tab):
    html = await tab.content()
    return parse_detail_data(html)


async def main():
    browser, tab = await init()
    try:
        for page in range(1, TOTAL_PAGE + 1):
            await scrape_index(page, tab)
            detail_urls = await parse_index(tab)
            for detail_url in detail_urls:
                await scrape_detail(detail_url, tab)
                data = await parse_detail(tab)
                logging.info(f'detail data:{data}')
    finally:
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
