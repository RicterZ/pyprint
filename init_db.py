# coding: utf-8

from lib.settings import database_type

def main():
	if database_type == 'MySQL':
		from init_mysql_db import init_database
	elif database_type == 'sqlte':
		from init_sqlite_db import init_database
	else:
		print '[*] Error: unsupported database type'
		return
	init_database()

if __name__ == '__main__':
	main()
