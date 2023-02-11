# _*_ coding: utf-8 _*_
# @Time: 2023/2/11 10:50
# @Author: lemon
# @File: 多任务协程demo
# @Project: WebCrawlerDevelopment
import asyncio
import aiohttp
import logging

from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

# api返回数据条数
PAGE_SIZE = 18
# 爬取列表页数
PAGE_COUNT = 10
# 最大请求并发数
CONCURRENCY = 10
# 请求超时时间，单位秒
TIMEOUT = 10
# 列表页url
INDEX_URL = 'https://spa5.scrape.center/api/book/?limit=18&offset={offset}'
# 详情页url
DETAIL_URL = 'https://spa5.scrape.center/api/book/{id}/'

# mongodb连接uri
MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'
# mongodb数据库名
MONGO_DB_NAME = 'books'
# mongodb文档名
MONGO_COLLECTION_NAME = 'books'

# 最大请求并发量控制为10
semaphore = asyncio.Semaphore(CONCURRENCY)


# 通用爬取接口
async def scrape_api(session: aiohttp.ClientSession, url):
    async with semaphore:
        try:
            logging.info(f'scraping {url}')
            async with session.get(url) as resp:
                return await resp.json()
        except aiohttp.ClientError:
            logging.error(f'error occurred while scraping {url}', exc_info=True)
        except asyncio.TimeoutError:
            logging.error(f'timeout error occurred while scraping {url}', exc_info=True)


# 爬取列表页，返回响应结果
async def scrape_index(session, page):
    url = INDEX_URL.format(offset=(page * PAGE_SIZE))
    return await scrape_api(session, url)


# 爬取详情页，将数据异步入库
async def scrape_detail(session, id):
    url = DETAIL_URL.format(id=id)
    res = await scrape_api(session, url)
    await save_data(data=res)


client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]


# 保存数据接口
async def save_data(data):
    logging.info(f'saving data {data}')
    if data:
        return await collection.update_one({
            'id': data.get('id')
        }, {
            '$set': data
        }, upsert=True)
    print(data)


# 入口
async def main():
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    session = aiohttp.ClientSession(timeout=timeout)
    scrape_index_tasks = [asyncio.ensure_future(scrape_index(session, page)) for page in range(0, PAGE_COUNT)]
    results = await asyncio.gather(*scrape_index_tasks)
    ids = []
    for res in results:
        for book in res['results']:
            ids.append(book['id'])

    scrape_detail_tasks = [asyncio.ensure_future(scrape_detail(session, id)) for id in ids]
    await asyncio.wait(scrape_detail_tasks)
    await session.close()


if __name__ == '__main__':
    # main()返回一个协程对象，run_until_complete()方法会将其封装成task对象
    # 同时也可以显示声明：task = loop.create_task(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
