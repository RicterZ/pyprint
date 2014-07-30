from settings import config
from functions import render_template


class BaseHandler(object):
    def render(self, template, title=None, **kwargs):
        return render_template(template, TITLE=title if title else config['username'],
                               config=config, **kwargs)


class IndexHandler(BaseHandler):
    def GET(self):
        return self.render('index.html')