# _*_ coding: utf-8 _*_
# @Time: 2023/2/10 12:19
# @Author: lemon
# @File: 4.4 MySQL存储
# @Project: WebCrawlerDevelopment
import pymysql

db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='spiders')


def create_db():
    cursor = db.cursor()
    cursor.execute('SELECT VERSION();')
    data = cursor.fetchone()
    print('Database version:', data)
    cursor.execute('CREATE DATABASE spiders DEFAULT CHARACTER SET utf8mb4')
    db.close()


def create_table():
    cursor = db.cursor()
    sql = '''
        CREATE TABLE IF NOT EXISTS students(
            id VARCHAR(255) NOT NULL ,
            name VARCHAR(255) NOT NULL ,
            age INT NOT NULL ,
            PRIMARY KEY (id)
        )
    '''
    cursor.execute(sql)
    db.close()


def insert():
    data = {
        'id': '2012003',
        'name': 'leo',
        'age': 21
    }
    table = 'students'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = f'INSERT INTO {table}({keys}) VALUES ({values})'
    cursor = db.cursor()
    try:
        print('execute sql:', sql)
        cursor.execute(sql, tuple(data.values()))
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    db.close()


def update():
    data = {
        'id': '2012001',
        'user': 'lemon',
        'age': 22
    }
    table = 'students'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = f'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE '
    update_str = ', '.join([f'{key}=%s' for key in data.keys()])
    sql += update_str

    cursor = db.cursor()

    try:
        print('execute sql:', sql)
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()


def delete():
    table = 'students'
    condition = 'age > 20'
    sql = f'DELETE FROM {table} WHERE {condition}'
    cursor = db.cursor()
    try:
        print('execute sql:', sql)
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()


def select():
    sql = 'SELECT * FROM students WHERE age >= 18'
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        print('Count:', cursor.rowcount)

        row = cursor.fetchone()
        while row:
            print('Row:', row)
            row = cursor.fetchone()

        # results = cursor.fetchall()
        # print('Results:', results)
        # print('Results Type:', type(results))
        # for row in results:
        #     print(row)

    except:
        print('error')


if __name__ == '__main__':
    # create_db()
    # create_table()
    # insert()
    # update()
    # delete()
    select()
    pass
