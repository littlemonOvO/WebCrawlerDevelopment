# _*_ coding: utf-8 _*_
# @Time: 2023/2/10 16:42
# @Author: lemon
# @File: spa6
# @Project: WebCrawlerDevelopment
import base64
import time
import hashlib
import requests
import asyncio
import aiohttp

from common.tools import time_statistics

'''
电影数据网站，数据通过 Ajax 加载，数据接口参数加密且有时间限制，
源码经过混淆，适合 JavaScript 逆向分析。
'''

INDEX_URL = 'https://spa6.scrape.center/api/movie/?limit=10&offset={offset}&token={token}'
DETAIL_URL = 'https://spa6.scrape.center/api/movie/{param}/?token={token}'
PAGE_COUNT = 5


def get_token(arr: list):
    timestamp = str(int(time.time()))
    li = arr.copy()
    li.append(timestamp)
    token = hashlib.sha1(','.join(li).encode('utf-8')).hexdigest()
    token = ','.join([token, timestamp])
    return base64.b64encode(token.encode('utf-8')).decode('utf-8')


def get_param(id):
    param_str = 'ef34#teuq0btua#(-57w1q5o5--j@98xygimlyfxs*-!i-0-mb' + str(id)
    return base64.b64encode(param_str.encode('utf-8')).decode('utf-8')


# session = aiohttp.ClientSession()


async def scrape_api(url):
    print(f'scraping {url}...')
    async with session.get(url) as resp:
        return await resp.json()


async def scrape_index(page):
    offset = page * 10
    url = INDEX_URL.format(offset=offset, token=get_token(['/api/movie']))
    return await scrape_api(url)


async def scrape_detail(id):
    param = get_param(id)
    token = get_token(['/api/movie/' + param])
    url = DETAIL_URL.format(param=param, token=token)
    res = await scrape_api(url)
    print(res)


@time_statistics('aiohttp')
async def run_by_aiohttp():
    global session
    session = aiohttp.ClientSession()
    index_tasks = [asyncio.ensure_future(scrape_index(page)) for page in range(0, PAGE_COUNT)]
    results = await asyncio.gather(*index_tasks)
    ids = []
    for res in results:
        for item in res['results']:
            ids.append(item['id'])

    detail_tasks = [asyncio.ensure_future(scrape_detail(id)) for id in ids]
    await asyncio.wait(detail_tasks)
    await session.close()


@time_statistics('requests')
def run_by_requests():
    arr = ['/api/movie']
    ids = []
    for page in range(0, PAGE_COUNT):
        offset = page * 10
        url = INDEX_URL.format(offset=offset, token=get_token(arr))
        resp = requests.get(url)
        for item in resp.json()['results']:
            ids.append(item['id'])

    for id in ids:
        param = get_param(id)
        token = get_token(['/api/movie/' + param])
        detail_url = DETAIL_URL.format(param=param, token=token)
        resp = requests.get(detail_url)
        print(resp.status_code)
        print(resp.json())


if __name__ == '__main__':
    run_by_requests()
    asyncio.get_event_loop().run_until_complete(run_by_aiohttp())
