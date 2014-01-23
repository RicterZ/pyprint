__author__ = 'Ricter'

from lib.utils import markdown_to_html, render, response
from lib.authentication import authentication
from lib.models import *
from lib.settings import *


class BaseHandler:
    def __init__(self):
        pass


class IndexHandler(BaseHandler):
    def GET(self):
        data = markdown_to_html(list_three_articles())
        return render("index.html", title='Ricter', data=data)


class ArticleHandler(BaseHandler):
    def GET(self, article_id):
        data = markdown_to_html(get_one_article(article_id))
        return render("index.html", title=data[0].title, data=data)

    def DELETE(self, article_id):
        @authentication
        def func():
            del_one_article(article_id)
            return response(204)
        return func()

    def PUT(self, article_id):
        @authentication
        def func():
            data = web.input(title='', content='')
            if not (data.title == '' or data.content == ''):
                update_one_article(article_id, data)
                return response(200, "Update success")
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
        return render("rss.xml", title='Ricter Blog', data=data)