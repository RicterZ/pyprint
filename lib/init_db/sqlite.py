#coding: utf-8
__author__ = 'Madimo'

import sqlite3
import datetime
from lib.settings import sqlite_path
from lib.utils import password_to_md5


def init_database():
    username = 'admin'
    password = 'admin'

    test_blog = '''
## 欢迎使用 PyPrint ##
PyPrint 是一个轻量级的博客系统，总之很轻量就是了。    
PyPrint 支持 **Markdown** 方式写作，并不支持插件、主题；代码写的也很烂。总之是我自用的。如果您觉得很难用实感抱歉。  
#### 这是一个测试标题 ####
这是一些测试的文本。这些文本并没有什么特别的含义。   

    def say_hello(name=None):
    	print 'Hello, %s!' % name if name else 'World'


    say_hello('Cee')

上面是一个写的很渣的程序，而且我还没测试能不能跑过。我总是感觉其中的`name if name else 'World'`有问题。  
推荐一些比较好的网站吧！  

+ 知乎：[http://www.zhihu.com](http://www.zhihu.com)  
+ V2EX：[http://www.v2ex.com](http://www.v2ex.com)  
+ Hacker News：[https://news.ycombinator.com](https://news.ycombinator.com)  

其中感觉 V2EX 的氛围很好。很喜欢。   
![QAQ](http://static.ricter.me/1.jpg)
总之感谢您的使用。如果有任何 Bug 请反馈给我，或者去 [Github](https://github.com) 提交 issue。   
* Ricter 敬上 *
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
            session char(32) default null
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
    db.execute("insert into tags(tag_name) values ('PyPrint')")

    # create a test blog
    db.execute('''insert into articles(title, date, content) 
    values (?, ?, ?)''', 
        (u'欢迎使用 PyPrint', str(datetime.datetime.now()).split('.')[0], test_blog.decode('utf-8')))
    db.execute("insert into articles_tags (article_id, tag_id) values (1, 1)")
    db.execute("insert into articles_tags (article_id, tag_id) values (1, 2)")

    # create default settings
    db.execute('''
        insert into user_data(username, blog_title, blog_description, blog_intro, blog_keyword, disqus_code, email)
        values (?, ?, ?, ?, ?, ?, ?)''', 
        (username, 'PyPrint', 'Here is My Blog!', u'初心を忘れず', 'PyPrint', '', 'root@yoursite.com'))

    # create account
    db.execute("insert into auth_user(username, password) values (?, ?)", (username, password_to_md5(password)))

    db.commit()
    db.close()

    print '[*] All done!'



if __name__ == '__main__':
    init_database()
