#!/usr/bin/python3
# -*- coding:utf-8 -*-
import time
import pymysql
import json

# 打开数据库连接
db = pymysql.connect("localhost", "root", "cqtddt@2016", "chat")
db.set_charset('utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


# 打开数据库
def open_db():
	global db,cursor
	# 打开数据库连接
	db = pymysql.connect("localhost", "root", "cqtddt@2016", "chat")
	db.set_charset('utf8')
	# 使用 cursor() 方法创建一个游标对象 cursor
	cursor = db.cursor()


# 创建表
def create_mysql_table():
	# 使用 execute() 方法执行 SQL，如果表存在则删除
	cursor.execute("DROP TABLE IF EXISTS user")

	# 使用预处理语句创建表
	sql = """CREATE TABLE user(user_id BIGINT primary key AUTO_INCREMENT NOT NULL, user_name CHAR(20), user_nick VARCHAR (100),user_hint VARCHAR (100),user_date VARCHAR (20)) DEFAULT CHARSET = utf8 """

	try:
		cursor.execute(sql)
		print("创建表成功")
		return True
	except:
		db.rollback()
		print("创建表失败")
		return False


# 关闭数据库
def close_joke_db():
	cursor.close()
	db.close


# 向数据库中插入
def insert_user_data(name, nick, hint):

	datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

	# SQL 插入语句
	sql = """INSERT INTO user(user_name,user_nick,user_hint,user_date) VALUES ('%s', '%s', '%s','%s') """
	try:
		# 执行sql语句
		cursor.execute(sql % (name, nick, hint, datetime))
		# 提交到数据库执行
		db.commit()
		print("加入新用户成功")
	except Exception:
	 	# 如果发生错误则回滚
	 	db.rollback()
	 	print("加入新用户失败")
	# 关闭数据库连接


# 更新数据库内容
def update_user_data(user_name, id):

	datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	# SQL 插入语句
	sql = """UPDATE user SET user_name = '%s', user_date = '%s' WHERE user_id = %d"""
	try:
		# 执行sql语句
		cursor.execute(sql % (user_name, datetime, id))
		# 提交到数据库执行
		db.commit()
		return True
	except Exception:
	 	# 如果发生错误则回滚
	 	db.rollback()
	return False


# {'code': 1, 'msg': '查询成功', 'data':
# [{'id': 1, 'title': '权限适配开发', 'content': '对融e购进行6.0权限适配，完成编译版本的升级', 'date': '2017-09-17 07:27:13', 'num': 0},
#  {'id': 3, 'title': '指纹登录', 'content': '进行指纹登录开发，并进行验证', 'date': '2017-09-17 07:27:13', 'num': 0},
# {'id': 4, 'title': '财富集市', 'content': '对财富集市进行功能设计，满足业务要求', 'date': '2017-09-17 07:27:13', 'num': 0}]}
# 查询任务数据，返回json字符串
def query_user_data():
	user_list = []
	user_item = {}
	# SQL 查询语句
	sql = "SELECT * FROM user"
	try:
		# 执行SQL语句
		cursor.execute(sql)
		# 获取所有记录列表
		results = cursor.fetchall()
		for row in results:
			user_data = {}

			user_id = row[0]
			user_data['id'] = user_id

			user_name = row[1]
			user_data['name'] = user_name

			user_nick = row[2]
			user_data['nick'] = user_nick

			hint = row[3]
			user_data['hint'] = hint

			user_date = row[4]
			user_data['date'] = user_date

			user_list.append(user_data)

		user_item['code'] = 1
		user_item['msg'] = '查询成功'
		user_item['data'] = user_list
	except:
		print("Error: unable to fetch data")
		user_item['code'] = 0
		user_item['msg'] = '查询失败'
		user_item['data'] = user_list
	return user_item


# 查询数据记录个数，返回json字符串
def query_joke_data_count():
	# SQL 查询语句
	sql = "select COUNT(*) from user"
	try:
		# 执行SQL语句
		cursor.execute(sql)
		# 获取所有记录列表
		result = cursor.fetchall()
		count = int(result[0][0])
	except:
		print("Error: unable to fetch data")
	return count


# 主方法
if __name__ == '__main__':

	#create_mysql_table()

	# insert_user_data("申建利", "shen", "jerry 好")
	# insert_user_data("郝高龙", "郝青燕", "龙")
	# insert_user_data("李志龙", "龙四", "龙四")
	# insert_user_data("吴佳健", "吴佳健", "佳健")
	# insert_user_data("阳阳", "明阳", "阳阳")
	insert_user_data("王凯", "王老道", "凯凯")

	count = query_joke_data_count()
	print(count)

	#update_user_data("申哥", 1)
	data = query_user_data()

	user_json = json.dumps(data, ensure_ascii=False)
	print(user_json)
	# close_joke_db()