__author__ = 'Ricter'

import MySQLdb
import datetime
import hashlib
from lib.settings import MySQL_user, MySQL_pass, MySQL_host, MySQL_DB

username = 'rixb'
password = 'rixb'


password = hashlib.md5(password).hexdigest()
print '[*] Connect to your MySQL host %s ...' % MySQL_host
conn = MySQLdb.connect(host=MySQL_host, user=MySQL_user, passwd=MySQL_pass)
cursor = conn.cursor()
print '[*] Create database %s ...' % MySQL_DB
cursor.execute("CREATE DATABASE %s" % MySQL_DB)
cursor.execute("USE %s" % MySQL_DB)
print '[*] Create table articles ...'
cursor.execute("create table articles (id INT(11) NOT NULL primary key auto_increment,title CHAR(50) NOT NULL,\
                date CHAR(40) NOT NULL,content LONGTEXT,click INT(11) DEFAULT '0')")
print '[*] Create table auth_user ...'
cursor.execute("create TABLE auth_user (id INT(11) NOT NULL primary key auto_increment,username CHAR(20) NOT NULL,\
                password CHAR(32) NOT NULL,session CHAR(32) NULL)")
print '[*] Create a test blog ...'
cursor.execute("insert into articles(title, date, content) values (%s, %s, %s)", \
               ('Hello, World!', str(datetime.datetime.now()).split('.')[0],'Welcome to My Blog!'))
print '[*] Create your account %s...' % username
cursor.execute("insert into auth_user(username, password) value (%s, %s)", (username, password))
conn.commit()
cursor.close()
conn.close()