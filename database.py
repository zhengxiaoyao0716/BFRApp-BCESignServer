#coding=UTF-8

def sqlite_execute(execStr, *params):
	cursor = con.execute(execStr, params)
	values = cursor.fetchall()
	cursor.close()
	return values

#Create
def create_tabs():
	sqlite_execute('CREATE TABLE aksk(ak TEXT, sk TEXT)')
	sqlite_execute('CREATE TABLE member(\
		flag varchar(255) NOT NULL UNIQUE, \
		name varchar(255) NOT NULL, \
		department varchar(255), \
		position varchar(255), \
		welcome varchar(255)\
	)')

#Insert
def insert_values():
	#aksk
	sqlite_execute('INSERT INTO aksk VALUES("", "")')
	#member
	sqlite_execute('INSERT INTO member (flag, name, department, position, welcome) VALUES("LaiYongGang", "赖永刚", "运营", "Boss", "刚哥好！刚哥威武！")')
	sqlite_execute('INSERT INTO member (flag, name, department, welcome) VALUES("ChenZheng", "陈正", "移动端", "逍遥来了啊")')
	sqlite_execute('INSERT INTO member (flag, name, department, welcome) VALUES("XueHan", "薛函", "前端", "欢迎大神！")')

#Select
def list_tabs():
	def print_sql_exec(tableName):
		print tableName + '\n' + sqlite_execute('SELECT * FROM ' + tableName).__str__() + '\n\n'
	
	#查看aksk
	print_sql_exec('aksk')
	print_sql_exec('member')

#Select， export
def export_data():
	from json import dumps
	export_sql_exec = lambda tableName, f : f.write(tableName + '\n' + dumps(sqlite_execute('SELECT * FROM ' + tableName), ensure_ascii = False) + '\n\n')
	
	with open('export.txt', 'a') as f :
		f.truncate()
		export_sql_exec('aksk', f)
		export_sql_exec('member', f)
	print u'\n结果已输出到 /export.txt 文件中'

#Drop
def delete_tabs():
	sqlite_execute('DROP TABLE aksk')
	sqlite_execute('DROP TABLE member')

if __name__ == '__main__':
	from sqlite3 import connect
	con = connect('BCESign.db')
	con.row_factory = lambda cur, row : dict((col[0], row[idx]) for idx, col in enumerate(cur.description))
	con.text_factory = str
	
	from sys import argv
	if len(argv) == 1 : list_tabs()
	elif argv[1] == 'create' :
		create_tabs()
		insert_values()
		print 'Complete'
	elif argv[1] == 'rebuild' :
		delete_tabs()
		create_tabs()
		insert_values()
		print 'Complete'
	elif argv[1] == 'delete' :
		delete_tabs()
		print 'Complete'
	elif argv[1] == 'export' :
		export_data()
	else : print 'Unknown'

	con.commit()
	con.close()