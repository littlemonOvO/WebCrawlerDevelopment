# _*_ coding: utf-8 _*_
# @Time: 2023/2/10 15:38
# @Author: lemon
# @File: MongoDB文档存储
# @Project: WebCrawlerDevelopment
import pymongo

# 连接数据库
client = pymongo.MongoClient(host='localhost', port=27017)
# 指定数据库
db = client['test']
# 指定集合
collection = db['students']


def insert():
    student = {
        'id': '20170101',
        'name': 'Jordan',
        'age': 20,
        'gender': 'male'
    }
    result = collection.insert_one(student)
    print(result)
    # 返回唯一标识_id
    print(result.inserted_id)

    student1 = {
        'id': '20170101',
        'name': 'Jordan',
        'age': 20,
        'gender': 'male'
    }

    student2 = {
        'id': '20170202',
        'name': 'Mike',
        'age': 21,
        'gender': 'male'
    }
    result = collection.insert_many([student1, student2])
    print(result)
    print(result.inserted_ids)


def select():
    # 查询单条数据
    print('查询单条数据')
    result = collection.find_one({
        'name': 'Mike'
    })
    print(type(result))
    print(result)

    # 查询多条数据
    print('查询多条数据')
    results = collection.find({'age': 20})
    for res in results:
        print(res)

    # 查询条件
    """
    符　　号	    含　　义	        示　　例
    $lt	        小于	    {'age': {'$lt': 20}}
    $gt	        大于	    {'age': {'$gt': 20}}
    $lte    	小于等于	    {'age': {'$lte': 20}}
    $gte    	大于等于	    {'age': {'$gte': 20}}
    $ne	        不等于	    {'age': {'$ne': 20}}
    $in	        在范围内	    {'age': {'$in': [20, 23]}}
    $nin    	不在范围内	{'age': {'$nin': [20, 23]}}
    """
    # 查询年龄大于20的数据
    print('查询年龄大于20的数据')
    results = collection.find({'age': {'$gt': 20}})
    for res in results:
        print(res)

    # 功能符号
    """
    符　　号	    含　　义	        示　　例	                                            示 例 含 义
    $regex	    匹配正则表达式	{'name': {'$regex': '^M.*'}}	                    name 以 M 开头
    $exists	    属性是否存在	    {'name': {'$exists': True}}	                        name 属性存在
    $type	    类型判断	        {'age': {'$type': 'int'}}	                        age 的类型为 int
    $mod	    数字模操作	    {'age': {'$mod': [5, 0]}}	                        年龄模 5 余 0
    $text	    文本查询	        {'$text': {'$search': 'Mike'}}	                    text 类型的属性中包含 Mike 字符串
    $where	    高级条件查询	    {'$where': 'obj.fans_count == obj.follows_count'}	自身粉丝数等于关注数
    """
    print('正则匹配名字以M开头的数据')
    results = collection.find({'name': {'$regex': '^M.*'}})
    for res in results:
        print(res)


def count():
    c = collection.count_documents({})
    print('Count:', c)
    c = collection.count_documents({'age': {'$lt': 21}})
    print('Count:', c)


def sort():
    # name按升序排列
    results = collection.find().sort('name', pymongo.ASCENDING)
    print([result['name'] for result in results])


def skip():
    # 偏移1个位置，从第二个元素开始取
    results = collection.find().sort('name', pymongo.ASCENDING).skip(1)
    print([result['name'] for result in results])
    # 限制个数
    results = collection.find().sort('name', pymongo.ASCENDING).limit(1)
    print([result['name'] for result in results])


def update():
    # condition = {'name': 'Jordan'}
    # student = collection.find_one(condition)
    # student['name'] = 'Kevin'
    # result = collection.update_one(condition, {'$set': student})
    # print(result)
    # print(result.matched_count, result.modified_count)

    condition = {'age': {'$gte': 20}}
    result = collection.update_many(condition, {'$inc': {'age': 1}})
    # print(result)
    print(result.matched_count, result.modified_count)


def delete():
    res = collection.delete_one({'name': 'lemon'})
    print(res.deleted_count)
    res = collection.delete_many({'age': {'$lt': 18}})
    print(res.deleted_count)


if __name__ == '__main__':
    # insert()
    # select()
    # count()
    # sort()
    # skip()
    # update()
    delete()
