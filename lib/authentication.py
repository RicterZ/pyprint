__author__ = 'Ricter'
import web
from lib.http_response import Forbidden
from lib.models import auth_check


def authentication(func):
    def has_permission():
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
        if has_permission():
            return _func
        else:
            def return_a_error():
                raise Forbidden
            return return_a_error
    return decorator(func)
