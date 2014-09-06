import tornado.web

from pyprint.handler import BaseHandler
from pyprint.models import User


class SignInHandler(BaseHandler):
    def get(self):
        return self.render('login.html', title='Sign in')

    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        if username and password:
            user = self.orm.query(User).filter(User.username==username).one()
            if user.check(password):
                self.set_secure_cookie('username', user.username)
                self.redirect('/kamisama/add/post')

        return self.redirect('/login')


class AddPostHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        pass

    @tornado.web.authenticated
    def post(self):
        pass


class AddLinkHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        pass

    @tornado.web.authenticated
    def post(self):
        pass