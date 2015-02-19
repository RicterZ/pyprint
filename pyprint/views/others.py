import urllib2
from pyprint.handler import BaseHandler


class AkarinHandler(BaseHandler):
    def get(self):
        return self.render('not_found.html', title='404 Not Found')


class NotFoundHandler(BaseHandler):
    def get(self, path):
        return self.redirect('/akarin')


class HitokotoHandler(BaseHandler):
    def get(self):
        hitokoto_url = 'http://api.hitokoto.us/rand?encode=js&charset=utf-8'
        self.write(urllib2.urlopen(hitokoto_url).read())
