# _*_ coding: utf-8 _*_
# @Time: 2023/2/12 10:01
# @Author: lemon
# @File: 7.6 Pyppeteer爬取实战
# @Project: WebCrawlerDevelopment
import asyncio
import logging
from pyppeteer import launch
from pyppeteer.errors import TimeoutError


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = 'https://spa2.scrape.center/page/{page}'
TIMEOUT = 10
TOTAL_PAGE = 10
WINDOW_WIDTH, WINDOW_HEIGHT = 1366, 768
HEADLESS = True


# 初始化
async def init():
    browser = await launch(headless=HEADLESS,
                           args=['--disable-infobars',
                                 f'--window-size={WINDOW_WIDTH}, {WINDOW_HEIGHT}'])
    tab = await browser.newPage()
    await tab.setViewport({'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT})
    return browser, tab


# 通用爬取接口
async def scrape_api(url, tab, selector):
    logging.info(f'scraping {url}...')
    try:
        await tab.goto(url)
        await tab.waitForSelector(selector, options={
            'timeout': TIMEOUT * 1000
        })
    except TimeoutError:
        logging.info(f'error occurred scraping {url}.', exc_info=True)


# 列表爬取接口
async def scrape_index(page, tab):
    url = INDEX_URL.format(page=page)
    await scrape_api(url, tab, 'div.item')


# 列表页解析接口
async def parse_index(tab):
    detail_urls = await tab.querySelectorAllEval('div.item a.name', 'nodes => nodes.map(node => node.href)')
    return detail_urls


# 详情页爬取接口
async def scrape_detail(url, tab):
    await scrape_api(url, tab, 'div.item img')


# 详情页解析接口
async def parse_detail(tab):
    name = await tab.querySelectorEval('div.item h2', 'node => node.innerText')
    categories = await tab.querySelectorAllEval('.item .categories span', 'nodes => nodes.map(node => node.innerText)')
    url = tab.url
    cover = await tab.querySelectorEval('.item img', 'node => node.src')
    score = await tab.querySelectorEval('.item .score', 'node => node.innerText')
    drama = await tab.querySelectorEval('.item .drama p', 'node => node.innerText')
    return {
        'url': url,
        'name': name,
        'categories': categories,
        'cover': cover,
        'score': float(score),
        'drama': drama
    }


# 主入口
async def main():
    browser, tab = await init()
    try:
        for page in range(1, TOTAL_PAGE + 1):
            await scrape_index(page, tab)
            detail_urls = await parse_index(tab)
            for detail_url in detail_urls:
                await scrape_detail(detail_url, tab)
                data = await parse_detail(tab)
                logging.info(f'detail data: {data}')
    finally:
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
