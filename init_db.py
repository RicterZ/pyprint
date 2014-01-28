# coding: utf-8

from lib.settings import database_type

def main():
    if database_type == 'mysql':
        import init_mysql_db
        init_mysql_db.init_database()
    elif database_type == 'sqlite':
        import init_sqlite_db
        init_sqlite_db.init_database()
    else:
        print '[*] Error: unsupported database type'

if __name__ == '__main__':
    main()

