#coding: utf-8
__author__ = 'Ricter'

import MySQLdb
import datetime
import hashlib
from lib.settings import MySQL_user, MySQL_pass, MySQL_host, MySQL_DB

def init_database():
    username = 'rixb'
    password = 'rixb'
    test_blog = """
#Welcome to My Blog!
This is rixb - a web.py blog system.   
It's RESTful and lightweight.    
Here is some test text.    
##Code

    def say_hello_world(name):
        if name:
            print "Hello, %s" % name 
        else:
            print "Hello World!"
    
    say_hello_world("Ricter")
    say_hello_world()

##Quote

> Hello World!    
> 你好世界！    
> こんにちは、世界！

##List

+ Python
    + Django
    + Web.py
    + Torando
+ HTML
+ CSS
+ Javascript
    + Node.js

##And more!
Thank you.
"""

    password = hashlib.md5(password).hexdigest()
    print '[*] Connect to your MySQL host %s ...' % MySQL_host
    conn = MySQLdb.connect(host=MySQL_host, user=MySQL_user, passwd=MySQL_pass)
    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute("set names utf8")
    cursor.execute("SET CHARACTER SET utf8")
    cursor.execute("SET character_set_connection=utf8")

    print "[*] Create database '%s' ..." % MySQL_DB
    cursor.execute("CREATE DATABASE %s default charset utf8 COLLATE utf8_general_ci" % MySQL_DB)
    cursor.execute("USE %s" % MySQL_DB)

    print "[*] Create table 'articles' ..."
    cursor.execute("""
        create table articles (
            id INT(11) NOT NULL primary key auto_increment,
            title CHAR(50) NOT NULL,
            date CHAR(40) NOT NULL,
            content LONGTEXT,
            click INT(11) DEFAULT 0
        )""")

    print "[*] Create table 'tags' ..."
    cursor.execute("""
        create TABLE tags (
            id INT(11) NOT NULL primary key auto_increment,
            tag_name CHAR(10) NOT NULL
        )""")

    print "[*] Create table 'articles_tags' ..."
    cursor.execute("""
        create TABLE articles_tags (
            id INT(11) NOT NULL primary key auto_increment,
            article_id INT(11) NOT NULL,
            tag_id INT(11) NOT NULL
        )""")

    print "[*] Create table 'auth_user' ..."
    cursor.execute("""
        create TABLE auth_user (
            id INT(11) NOT NULL primary key auto_increment,
            username CHAR(20) NOT NULL,
            password CHAR(32) NOT NULL,
            session CHAR(32) NULL)
        """)

    print "[*] Create table 'user_data' ..."
    cursor.execute("""
        create TABLE user_data (
            id INT(11) NOT NULL primary key auto_increment,
            username CHAR(20) NOT NULL,
            blog_title CHAR(40) NOT NULL,
            blog_intro LONGTEXT,
            blog_keyword CHAR(40) NOT NULL,
            disqus_code LONGTEXT,
            email CHAR(50) NOT NULL,
            blog_description LONGTEXT)
        """)

    print "[*] Create table 'friends_link' ..."
    cursor.execute("""
        create TABLE friends_link (
            id INT(11) NOT NULL primary key auto_increment,
            friend_name CHAR(30) NOT NULL,
            link CHAR(50) NOT NULL)
        """)

    print "[*] Add some tags ..."
    cursor.execute("insert into tags(tag_name) values ('HelloWorld')")
    cursor.execute("insert into tags(tag_name) values ('rixb')")

    print "[*] Create a test blog ..."
    cursor.execute("insert into articles(title, date, content) values (%s, %s, %s)",
                    ('Hello, World!', str(datetime.datetime.now()).split('.')[0], test_blog.decode('utf-8')))
    cursor.execute("insert into articles_tags(article_id, tag_id) values (1, 1)")
    cursor.execute("insert into articles_tags(article_id, tag_id) values (1, 2)")

    print "[*] Create default setting ..."
    cursor.execute("insert into user_data(username, blog_description, blog_intro, blog_keyword, disqus_code, email) values \
    (%s, %s, %s, %s, %s, %s)", (username, 'Here is My Blog!', 'My Blog :)', 'rixb', '', 'root@yoursite.com'))

    print "[*] Create your account %s..." % username
    cursor.execute("insert into auth_user(username, password) values (%s, %s)", (username, password))
    conn.commit()
    cursor.close()
    conn.close()


    if __name__ == '__main__':
        init_database()
