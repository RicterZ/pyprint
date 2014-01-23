# -*- coding:utf-8 -*-
import web
import jinja2 as jj
import local_settings

web.config.debug = False
templates_path = 'templates'
MySQL_host = 'ricter.info'
MySQL_user = 'ricter'
#MySQL_pass = ''
#MySQL_DB = ''

db = web.database(host=MySQL_host, dbn='mysql', db=MySQL_DB, user=MySQL_user, pw=MySQL_pass)
env = jj.Environment(loader=jj.FileSystemLoader('templates'))