from pyprint.handler import BaseHandler
from pyprint.models import User


class SignInHandler(BaseHandler):
    def get(self):
        return self.render('signin.html', title='Sign in')

    def post(self):
        pass