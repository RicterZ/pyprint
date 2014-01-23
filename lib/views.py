__author__ = 'Ricter'

import json
from lib.utils import markdown_to_html, render
from lib.http_response import HTTP_RESPONSE
from lib.authentication import authentication
from lib.models import *
from lib.settings import *


def response(status, message=""):
    if status == 200:
        web.header('Content-Type', 'application/json')
        return json.dumps({"message": message})
    else:
        raise HTTP_RESPONSE[status]


class BaseHandler:
    def __init__(self):
        pass


class IndexHandler(BaseHandler):
    def GET(self):
        data = markdown_to_html(list_three_articles())
        return render("index.html", title='Ricter Blog', data=data)


class ArticleHandler(BaseHandler):
    def GET(self, article_id=None):
        if not article_id:
            return response(403)
        post_format = web.input(format='').format
        data = markdown_to_html(get_a_article(article_id))
        try:
            data = data[0]
        except IndexError:
            return response(404)
        if post_format == 'json':
            return response(200, data)
        else:
            return render("index.html", title=data.title, data=[data])

    def DELETE(self, article_id):
        @authentication
        def func():
            if del_a_article(article_id):
                return response(204)
            else:
                return response(404)
        return func()

    def PUT(self, article_id):
        @authentication
        def func():
            data = web.input(title='', content='')
            if not (data.title == '' or data.content == ''):
                if update_a_article(article_id, data):
                    return response(200, "Update success")
                else:
                    return response(404)
        return func()

    def POST(self):
        @authentication
        def func():
            data = web.input(title='', content='')
            if not (data.title == '' or data.content == ''):
                post_a_article(data)
                return response(201)
        return func()


class LoginHandler(BaseHandler):
    def GET(self):
        return render("signin.html", title="Login")

    def POST(self):
        data = web.input(username='', password='')
        if check_login(data):
            web.setcookie("username", data.username, expires="99999")
            web.setcookie("session", save_session(data.username), expires="99999")
            return response(200, "Authentication success")
        else:
            return response(401)


class TimelineHandler(BaseHandler):
    def GET(self):
        data = timeline_list()
        return render("timeline.html", title="Timeline", data=data)


class ManageHandler(BaseHandler):
    def GET(self):
        @authentication
        def func():
            pass
        return func()


class RssHandler(BaseHandler):
    def GET(self):
        web.header('Content-type', "text/xml; charset=utf-8")
        data = markdown_to_html(list_all_articles())
        return render("rss.xml", title='Ricter Blog', data=data, url=web.ctx.host)