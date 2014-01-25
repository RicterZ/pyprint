MySQL_host = 'localhost'
MySQL_user = 'root'
MySQL_pass = ''
MySQL_DB = ''

from local_settings import *
import web
import jinja2 as jj

web.config.debug = False
db = web.database(host=MySQL_host, dbn='mysql', db=MySQL_DB, user=MySQL_user, pw=MySQL_pass)
env = jj.Environment(loader=jj.FileSystemLoader('templates'))