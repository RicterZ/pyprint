import web
import jinja2 as jj

# database_type = 'mysql' or 'sqlite'
database_type = 'sqlite'
# these values is for mysql
MySQL_host = 'localhost'
MySQL_user = 'root'
MySQL_pass = ''
MySQL_DB = ''
# these values is for sqlite
sqlite_path = 'rixb.db3'

# if you are a developer, you should set web.config.debug = True
web.config.debug = False

#from local_settings import *

if database_type == 'mysql':
    db = web.database(host=MySQL_host, dbn='mysql', db=MySQL_DB, user=MySQL_user, pw=MySQL_pass)
elif database_type == 'sqlite':
    db = web.database(dbn='sqlite', db=sqlite_path)

env = jj.Environment(loader=jj.FileSystemLoader('templates'), autoescape=True)
