#coding: utf-8
__author__ = 'Madimo'

import sqlite3
import datetime
from lib.settings import sqlite_path
from lib.utils import password_to_md5


def init_database():
    username = 'rixb'
    password = 'rixb'

    test_blog = '''
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
'''

    print '[*] Create database ...'

    db = sqlite3.connect(sqlite_path)

    db.execute('''
        create table articles (
            id integer not null primary key autoincrement,
            title char(50) not null,
            date char(40) not null,
            content longtext,
            click int(11) default 0
        )
    ''')

    db.execute('''
        create table tags (
            id integer not null primary key autoincrement,
            tag_name char(10) not null
        )
    ''')

    db.execute('''
        create table articles_tags (
            id integer not null primary key autoincrement,
            article_id int(11) not null,
            tag_id int(11) not null
        )  
    ''')

    db.execute('''
        create table auth_user (
            id integer not null primary key autoincrement,
            username char(20) not null,
            password char(32) not null,
            session char(32) null
        )
    ''')

    db.execute('''
        create table user_data (
            id integer not null primary key autoincrement,
            username char(20) not null,
            blog_title char(40) not null,
            blog_intro longtext,
            blog_keyword char(40) not null,
            disqus_code longtext,
            email char(50) not null,
            blog_description longtext
        )
    ''')

    db.execute('''
        create table friends_link (
            id integer not null primary key autoincrement,
            friend_name char(30) not null,
            link char(50) not null
        )
    ''')

    # add some tags
    db.execute("insert into tags(tag_name) values ('HelloWorld')")
    db.execute("insert into tags(tag_name) values ('rixb')")

    # create a test blog
    db.execute('''insert into articles(title, date, content) 
    values (?, ?, ?)''', 
        ('Hello World', str(datetime.datetime.now()).split('.')[0], test_blog.decode('utf-8')))
    db.execute("insert into articles_tags (article_id, tag_id) values (1, 1)")
    db.execute("insert into articles_tags (article_id, tag_id) values (1, 2)")

    # create default settings
    db.execute('''
        insert into user_data(username, blog_title, blog_description, blog_intro, blog_keyword, disqus_code, email)
        values (?, ?, ?, ?, ?, ?, ?)''', 
        ('rixb', 'rixb', 'Here is My Blog!', 'My Blog :)', 'rixb', '', 'root@yoursite.com'))

    # create account
    db.execute("insert into auth_user(username, password) values (?, ?)", (username, password_to_md5(password)))

    db.commit()
    db.close()

    print '[*] All done!'



if __name__ == '__main__':
    init_database()
