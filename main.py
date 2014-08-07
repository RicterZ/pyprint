#coding: utf-8
from lib.urls import urlpatterns
from lib.functions import load_sqlalchemy
from lib.handles import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = web.application(urlpatterns, globals())
app.add_processor(load_sqlalchemy)

if __name__ == "__main__":
    app.run()