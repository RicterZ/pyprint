#coding: utf-8

try:
    from localsettings import connect_str, cookie_secret
except ImportError:
    raise Exception('Please add connect_str and cookie_secret in localsettings.py')



# website settings
username = 'Ricter'
email = 'RicterZheng@gmail.com'
title = 'Ricter\'s Blog'
motto = u'初心を忘れず'
disqus_shortname = 'ricterblog2'

# themes name
theme = 'clean'

# development
debug = True


analytics_code = '''
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-53662402-1', 'auto');
  ga('send', 'pageview');
'''

post_of_page = 3


try:
    module = __import__('themes.%s.config' % theme, globals(), locals(), ['*'])
    for k in dir(module):
        locals()[k] = getattr(module, k)
except ImportError:
    pass

