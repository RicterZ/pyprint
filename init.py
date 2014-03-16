# coding: utf-8
from lib.settings import database_type


def main():
    if database_type == 'mysql':
        from lib.init_db.mysql import init_database
    elif database_type == 'sqlite':
        from lib.init_db.sqlite import init_database
    else:
        print '[*] Error: unsupported database type'
        return
    init_database()


if __name__ == '__main__':
    main()


