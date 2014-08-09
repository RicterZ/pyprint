from pyprint.handler import BaseHandler


class AkarinHandler(BaseHandler):
    def get(self):
        return self.render('not_found.html')


class NotFoundHandler(BaseHandler):
    def get(self, path):
        return self.redirect('/akarin')