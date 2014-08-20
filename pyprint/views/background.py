import tornado.web

from pyprint.handler import BaseHandler
from pyprint.models import User


class SignInHandler(BaseHandler):
    def get(self):
        return self.render('login.html', title='Sign in')

    def post(self):
        pass


class AddPostHandler(BaseHandler):
    def get(self):
        pass

    def post(self):
        pass


class AddLinkHandler(BaseHandler):
    def get(self):
        pass

    def post(self):
        pass