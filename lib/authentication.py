__author__ = 'Ricter'
import web
from lib.utils import response
from lib.models import auth_check


def authentication(func):
    def is_permission():
        try:
            cookies = web.cookies()
            username = cookies.username
            session = cookies.session
            if not username or not session:
                return False
            return auth_check(username, session)
        except AttributeError:
            return False

    def decorator(_func=func):
        if is_permission():
            return _func
        else:
            def return_a_error():
                return response(403)
            return return_a_error
    return decorator(func)