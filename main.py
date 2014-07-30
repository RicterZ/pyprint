import web
from lib.urls import urlpatterns
from lib.handles import *


app = web.application(urlpatterns, globals())
if __name__ == "__main__":
    app.run()