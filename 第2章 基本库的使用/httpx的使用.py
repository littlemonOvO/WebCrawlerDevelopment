# _*_ coding: utf-8 _*_
# @Time: 2023/2/9 16:06
# @Author: lemon
# @File: httpx的使用
# @Project: WebCrawlerDevelopment
import asyncio

import requests

import httpx

# httpx:一个支持HTTP2.0的请求库

url = 'https://spa16.scrape.center/'


def use_requests():
    resp = requests.get(url)
    print(resp.status_code)


def use_httpx():
    # 开启http2.0支持
    client = httpx.Client(http2=True)
    resp = client.get(url)
    print(resp.status_code)

    # GET请求
    r = httpx.get('https://www.httpbin.org/get', params={'name': 'lemon'})
    # POST请求
    r = httpx.post('https://www.httpbin.org/post', data={'name': 'lemon'})
    # PUT请求
    r = httpx.put('https://www.httpbin.org/put')
    # DELETE请求
    r = httpx.put('https://www.httpbin.org/delete')

    # Client对象，类似于requests.Session
    headers = {}
    with httpx.Client(headers=headers, http2=True) as client:
        resp = client.get(url)
        print(resp.status_code)
        print(resp.http_version)

    # 异步请求
    async def fetch(url):
        async with httpx.AsyncClient(http2=True) as client:
            resp = await client.get(url)
            print(resp.status_code)

    asyncio.run(fetch(url))


if __name__ == '__main__':
    # use_requests()
    use_httpx()
