#coding: utf-8
import web
from hashlib import md5

# the path of templates
templates = '../templates'

# web.py debug mode
debug = False

db_config = {
    'db_type': 'sqlite',
    'db_user': 'root',
    'db_pass': '123456',
    'db_name': 'sqlite.db',
    'port': 3306,
    'host': 'localhost',
}

config = {
    'username': 'Ricter',

    # information of yourself
    'email': 'RicterZheng@gmail.com',
    'motto': u'初心を忘れず',
    'title': u'Ricter 的 Blog',
    'disqus_shortname': 'ricterblog2',

    # analytics_code
    'analytics_code': '''
        (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
        (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
        m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
        })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
        ga('create', 'UA-53662402-1', 'auto');
        ga('send', 'pageview');''',
}


# don't modify 0^0
config['email_md5'] = md5(config['email'].lower()).hexdigest()

web.config.debug = debug

