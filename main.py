# -*- coding:utf-8 -*-
from lib.urls import *
from lib.views import *

application = web.application(urls, globals()).wsgifunc()
app = web.application(urls, globals())
app.add_processor(load_sqlalchemy)

if __name__ == "__main__":
    app.run()
