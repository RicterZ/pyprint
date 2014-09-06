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
            user = self.orm.Query(User.username == username).one()
            if user.check(password):
                token = user.generate_token()
                self.set_secure_cookie('username', user.username)
                self.set_secure_cookie('token', token)
                self.redirect('/kamisama/add/post')

        return self.redirect('/login')


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