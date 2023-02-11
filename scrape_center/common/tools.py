# _*_ coding: utf-8 _*_
# @Time: 2023/2/11 17:23
# @Author: lemon
# @File: tools
# @Project: WebCrawlerDevelopment

import time


# 统计耗时
def time_statistics(name=None):
    def wrapper(func):
        def inner(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            end = time.time()
            param = func.__name__ if not name else name
            print(f'{param} cost {end - start:.2f}s')
            return res

        return inner

    return wrapper
