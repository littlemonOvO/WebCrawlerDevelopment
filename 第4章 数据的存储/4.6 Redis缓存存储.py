# _*_ coding: utf-8 _*_
# @Time: 2023/2/10 16:26
# @Author: lemon
# @File: 4.6 Redis缓存存储
# @Project: WebCrawlerDevelopment
from redis import StrictRedis, ConnectionPool

pool = ConnectionPool(host='localhost', port=6379, db=0)
redis = StrictRedis(connection_pool=pool)


# 键操作
def key_operation():
    # 判断一个键是否存在
    print(redis.exists('name1'))
    # 删除一个键
    print(redis.delete('name3'))
    # 判断键类型
    print(redis.type('name1'))
    # 获取所有符合规则的键
    print(redis.keys('n*'))
    # 获取随机一个键
    print(redis.randomkey())
    # 对键重命名
    print(redis.rename('name1', 'name'))
    # 获取当前数据库键的数目
    print(redis.dbsize())
    # 设定键的过期时间，单位秒
    redis.expire('name', 2)
    # 获取键的过期时间，单位秒
    print(redis.ttl('name'))
    # 将键移动到其他数据库
    redis.move('name', 2)
    # 删除当前所选数据库中的所有键
    redis.flushdb()
    # 删除所有数据库中的所有键
    redis.flushall()


# 字符串操作
def string_operation():
    # 将数据库中指定键名对应的键值赋值为字符串value
    redis.set('name1', 'Mike')
    # 返回数据库中指定的键名对应的键值
    print(redis.get('name'))
    # 将数据库中指定键名对应的键值赋值为字符串value并返回上次的value
    print(redis.getset('name1', 'Kevin'))
    # 返回由多个键名对应的value组成的列表
    print(redis.mget(['name', 'name1', 'name2']))
    # 如果不存在指定的键值对，则更新value。否则保持不变
    print(redis.setnx('name', 'asd'))
    # 设置键名对应的键值为字符串类型的value，并指定此键值的有效期
    # 将name这个键的值设置为zxc，有效期为1秒
    redis.setex('name', time=1, value='zxc')
    # 设置指定键名对应的键值的子字符串
    # 在name的键值的6号索引为补充hello子字符串
    redis.setrange('name', offset=6, value='hello')
    # 批量赋值
    redis.mset({'name1': 'Durant', 'name2': 'James'})
    # 指定键名不存在时才批量赋值
    redis.msetnx({'name1': 'Durant', 'name2': 'James'})
    # 对指定键名对应键值做增值操作，默认增1。键名不存在时自动创建并将键值设为amount
    redis.incr('age', amount=20)
    # 对指定键名对应键值做减值操作，默认减1。键名不存在时自动创建并将键值设为amount
    redis.decr('age', amount=20)
    # 对指定键名对应的键值附加字符串value
    redis.append('name', value='?')


# 列表操作
# 列表元素可重复，且可以从两端存储
def list_operation():
    # 在指定键名列表末尾添加value，可传入多个value
    redis.rpush('li', 1, 2, 3)
    # 在指定键名列表头部添加value，可传入多个value
    redis.lpush('li', 4, 5, 6)
    # 返回指定键名列表长度
    print(redis.llen('li'))
    # 返回指定键名列表从索引start到索引end之间的元素
    print(redis.lrange('li', start=1, end=3))
    # 截取指定键名列表，保留从索引start到索引end之间的元素（包括两个索引所在位置的元素）
    redis.ltrim('li', 0, 0)
    # 返回指定键名列表中index位置的元素
    print(redis.lindex('li', index=2))
    # 给列表的指定index位置元素赋值，越界时报错
    redis.lset('li', index=0, value=0)
    # 删除指定键名列表中count个值为value的元素
    redis.lrem('li', count=2, value=3)
    # 返回并删除指定列表中的首元素
    redis.lpop('li')
    # 返回并删除指定列表中的尾元素
    redis.rpop('li')


# 集合操作
# 集合中的元素不重复
def set_operation():
    # 向指定键名的集合中添加元素
    redis.sadd('tags', 'Book', 'Tea', 'Coffee')
    # 从指定键名的集合中删除元素
    redis.srem('tags', 'Book')
    # 随机返回并删除指定集合中的一个元素
    print(redis.spop('tags'))
    # 将一个集合中的指定元素移动到另一个集合中
    redis.smove(src='tags', dst='tags2', value='Coffee')
    # 返回指定集合中的元素个数
    print(redis.scard('tags'))
    # 返回指定集合中的所有元素
    print(redis.smembers('tags'))
    # 随机返回指定集合中的一个元素但不删除该元素
    print(redis.srandmember('tags'))
    # 判断指定集合中是否存在某元素
    print(redis.sismember('tags', 'Book'))

    # 其余求合集、交集、差集的方法...


# 有序集合操作
# 相比于集合多了一个分数字段，可利用分数对集合元素进行排序
def ordered_set_operation():
    # 向指定有序集合添加元素，元素存在时更新各元素顺序
    redis.zadd('grade', {'Bob': 100, 'Mike': 98})
    # 删除指定有序集合中的某元素
    redis.zrem('grade', 'Mike')
    # 返回指定有序集合中value元素的排名（对各元素的score从小到大排序）
    print(redis.zrank('grade', 'Amy'))
    # 返回指定有序集合中value元素的倒数排名（对各元素的score从大到小排序）
    redis.zrevrank('grade', 'Amy')
    # 返回指定有序集合中的元素个数
    redis.zcard('grade')
    # 返回指定有序集合中给定名次区间内的元素（对各元素的score从大到小排序）
    redis.zrevrange('grade', start=0, end=3, withscores=True)
    # 返回指定有序集合中score在给定区间内的元素，可指定元素个数、起始索引和是否返回分数信息
    redis.zrangebyscore('grade', min=80, max=95)
    # 返回指定有序集合中score在给定区间内的元素个数
    redis.zcount('grade', min=80, max=95)
    pass


# 散列操作
def hash_operation():
    # 向指定散列表中添加映射
    redis.hset('price', key='cake', value=5)
    # 散列表中不存在给定映射时才添加此映射
    redis.hsetnx('price', key='book', value=6)
    # 返回指定散列表中key对应的键值
    redis.hget('price', key='cake')
    # 返回指定散列表中各个键名对应的键值
    redis.hmget('price', ['apple', 'orange'])
    # 向指定散列表中批量添加映射
    # redis.hmset('price', {'banana': 2, 'pear': 6})
    redis.hset('price', mapping={'banana': 2, 'pear': 6})
    # 获取指定散列表中的所有映射键名
    redis.hkeys('price')
    # 获取指定散列表中的所有映射键值
    redis.hvals('price')
    # 获取指定散列表中的所有映射键值对
    redis.hgetall('price')


if __name__ == '__main__':
    # key_operation()
    # string_operation()
    # list_operation()
    # ordered_set_operation()
    hash_operation()
