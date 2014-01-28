__author__ = 'Ricter'

from lib.settings import *
from utils import clean_input, now, password_to_md5, make_session, markdown_to_html


def list_three_articles():
    data = db.select('articles', where='1', limit=3, order='id desc')
    return data


def list_all_articles():
    data = db.select('articles', where='1', order='id desc')
    return data


def get_a_article(article_id):
    data = db.select('articles', where='id=%d' % int(article_id))
    return data


def del_a_article(article_id):
    data = db.delete('articles', where='id=%d' % int(article_id))
    db.delete('articles_tags', where='article_id=%d' % int(article_id))
    return data


def update_a_article(article_id, data):
    db.update('articles', where='id=%d' % int(article_id), title=data.title,
              date=now(), content=data.content)
    old_tags = [tag.tag_id for tag in get_tags_by_article(article_id)]
    new_tags = data.tag.split(',')
    for tag in old_tags:
        if tag not in new_tags:
            remove_tag(article_id, tag)
        else:
            new_tags.remove(tag)
    for tag in new_tags:
        tag_id = add_tag(tag)
        if tag_id:
            add_article_tag(article_id, tag_id)
    return data


def post_a_article(data):
    article_id = db.insert('articles', title=data.title, content=data.content, date=now())
    for tag in data.tag.split(','):
        tag_id = add_tag(tag)
        add_article_tag(article_id, tag_id)


def get_tag(tag_id):
    data = db.select('tags', where="id=%d" % int(tag_id))[0]
    return data


def get_articles_by_tag(tag_id):
    tag = get_tag(tag_id)
    tag_article = db.select('articles_tags', where='tag_id=%d' % int(tag.id))
    data = [markdown_to_html(get_a_article(article.article_id))[0] for article in tag_article]
    return data[::-1]


def get_tags_by_article(article_id):
    data = db.select('articles_tags', where='article_id=%d' % int(article_id))
    return data


def remove_tag(article_id, tag_id):
    db.delete('articles_tags', where="article_id=%d and tag_id=%d" % (int(article_id), int(tag_id)))


def get_tag_by_name(tag_name):
    #SQL Injection!!!
    data = db.select('tags', where="tag_name='%s'" % tag_name)
    return data


def get_tag_for_articles(articles):
    for item in articles:
        item.tag = [get_tag(tag.tag_id) for tag in get_tags_by_article(item.id)]
    return articles


def add_tag(tag_name):
    if not tag_name:
        return
    tag = get_tag_by_name(tag_name)
    if tag:
        return tag[0].id
    else:
        tag_id = db.insert('tags', tag_name=tag_name)
        return tag_id


def add_article_tag(article_id, tag_id):
    tags = get_tags_by_article(article_id)
    for tag in tags:
        if int(tag_id) == int(tag.id):
            return
    db.insert('articles_tags', article_id=article_id, tag_id=tag_id)


def timeline_list():
    data = db.select('articles', where='1', order='id desc', what="title, date, id")
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


def get_user_data():
    data = db.select('user_data', where="1", limit="1")[0]
    return data


def get_friends_link():
    data = db.select('friends_link', where="1")
    return data

def search_article(kw):
    data = db.select('articles', where="title='%%s%' or content='%%s%'" % (str(kw), str(kw)))
    return data
