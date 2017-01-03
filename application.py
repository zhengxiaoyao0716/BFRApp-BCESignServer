#coding=UTF-8

from flask import Flask, g, render_template, request
from json import dumps

app = Flask(__name__)


###############################操作数据###############################
##字典游标
def dict_factory(cursor, row):
    return dict((col[0], row[idx]) for idx, col in enumerate(cursor.description))

#每个route前，打开连接，配置连接
@app.before_request
def before_request():
	import sqlite3
	g.db = sqlite3.connect('BCESign.db')
	g.db.row_factory = dict_factory
	g.db.text_factory = str

#每个route后， 提交修改，关闭连接
@app.teardown_request
def teardown_request(exception):
	g.db.commit()
	g.db.close()

##执行查询，并取得查询结果
def sqlite_execute(execStr, *params):
	cursor = g.db.execute(execStr, params)
	values = cursor.fetchall()
	cursor.close()
	return values

##############################验证加密##############################
#密匙验证
#@params accessKeyId ak
#@params authStringPrefix authStringPrefix
@app.route('/bce/get_sign', methods = ['POST'])
def get_sign():
	secretAccessKey = sqlite_execute('SELECT sk FROM aksk WHERE ak == "%s"'%(request.form['accessKeyId']))[0]['sk']
	import hmac
	import hashlib
	if (secretAccessKey) :
		signingKey = hmac.new(secretAccessKey.__str__(), request.form['authStringPrefix'], hashlib.sha256).hexdigest().__str__()
		return signingKey
	else :
		return 'Failed'

'''
###############################成员管理###############################
#添加成员
#@params flag 唯一标识符
#@params name 可读的名字
#@params department 部门
#@params position 职位
#@params welcome 问候语
@app.route('/member/add', methods = ['POST'])
def add_member():
	sqlite_execute('INSERT INTO member * VALUES(?, ?, ?, ?, ?)',
		request.form['flag'], request.form['name'], request.form['department'], request.form['position'], request.form['welcome']
	)
	return 'Complete'

#删除成员
#@params flag 唯一标识符
@app.route('/member/delete', methods = ['POST'])
def delete_member():
	sqlite_execute('DELETE FROM member WHERE flag == ?', request.form['flag'])
	return 'Complete'

#修改成员
#@params department 部门
#@params position 职位
#@params welcome 问候语
@app.route('/member/update', methods = ['POST'])
def update_member():
	sqlite_execute('UPDATE member SET name == ?, department == ?, position == ?, welcome == ? WHERE flag == ?',
		request.form['name'], request.form['department'], request.form['position'], request.form['welcome'], request.form['flag']
	)
	return 'Complete'

#查看成员
#@params flag
@app.route('/member/list', methods = ['POST'])
def list_member():
	pass
'''


if __name__ == '__main__':
	#app.run(host = "123.57.72.138", port = 6000)
	app.run(debug = True)