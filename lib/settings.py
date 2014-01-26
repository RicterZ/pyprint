import web
import jinja2 as jj

MySQL_host = 'localhost'
MySQL_user = 'root'
MySQL_pass = ''
MySQL_DB = ''
web.config.debug = False
#if you are a developer, you should set web.config.debug = True

from local_settings import *

db = web.database(host=MySQL_host, dbn='mysql', db=MySQL_DB, user=MySQL_user, pw=MySQL_pass)
env = jj.Environment(loader=jj.FileSystemLoader('templates'))