__author__ = 'Ricter'

from lib.settings import *
from utils import clean_input, now, password_to_md5, make_session


def list_three_articles():
    data = db.select('articles', where='1', limit=6, order='id desc')
    return data


def list_all_articles():
    data = db.select('articles', where='1', order='id desc')
    return data


def get_one_article(article_id):
    data = db.select('articles', where='id=%d' % int(article_id))
    return data


def del_one_article(article_id):
    db.delete('articles', where='id=%d' % int(article_id))


def update_one_article(article_id, data):
    db.update('articles', where='id=%d' % int(article_id), title=data.title,
              date=now(), content=data.content)


def post_a_article(data):
    db.insert('articles', title=data.title, content=data.content, date=now())


def timeline_list():
    data = db.select('articles', where='1', order='id desc', what="title, date")
    return data

def check_login(data):
    try:
        user_data = db.select('auth_user', where="username='%s'" % clean_input(data.username))[0]
        if password_to_md5(data.password) == user_data.password:
            return True
        else:
            return False
    except IndexError:
        return False


def save_session(username):
    session = make_session()
    db.update('auth_user', where="username='%s'" % clean_input(username), session=session)
    return session


def auth_check(username, session):
    data = db.select('auth_user', where="username='%s'" % clean_input(username))[0]
    return str(data.session) == str(session)
