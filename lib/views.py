__author__ = 'Ricter'

import json
from lib.utils import markdown_to_html, render, article_to_storage, clean_input
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
        data = get_user_data()
        self.NAME = data.username
        self.INTRO = data.blog_intro
        self.DISQUS = data.disqus_code
        self.EMAIL = data.email
        self.FRIENDS = get_friends_link()
        self.KEYWORD = data.blog_keyword
        self.DESCRIPTION = data.blog_description

    def render(self, template, **kwargs):
        return render(template, NAME=self.NAME, EMAIL=self.EMAIL, FRIENDS=self.FRIENDS,
                      INTRO=self.INTRO, **kwargs)


class IndexHandler(BaseHandler):
    def GET(self):
        data = get_tag_for_articles(markdown_to_html(list_three_articles()))
        return self.render("index.html", title=self.NAME, data=data)


class ArticleHandler(BaseHandler):
    def GET(self, article_id=None):
        if not article_id:
            return response(403)
        web_input = web.input(format='', raw='false')
        post_format = web_input.format
        raw = web_input.raw
        if raw == 'true':
            data = get_tag_for_articles(article_to_storage(get_a_article(article_id)))
        else:
            data = get_tag_for_articles(markdown_to_html(get_a_article(article_id)))

        try:
            data = data[0]
        except IndexError:
            return response(404)
        if post_format == 'json':
            return response(200, data)
        else:
            return self.render("index.html", title=data.title, data=[data],
                               DISQUS=self.DISQUS)

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
            data = web.input(title='', content='', tag='')
            if not (data.title == '' or data.content == ''):
                if update_a_article(article_id, data):
                    return response(200, "Update success")
                else:
                    return response(404)
        return func()

    def POST(self):
        @authentication
        def func():
            data = web.input(title='', content='', tag='')
            if not (data.title == '' or data.content == ''):
                post_a_article(data)
                return response(201)
        return func()


class LoginHandler(BaseHandler):
    def GET(self):
        return self.render("signin.html", title="Login")

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
        return self.render("timeline.html", title="Timeline", data=data)


class TagHandler(BaseHandler):
    def GET(self, tag_id):
        data = get_tag_for_articles(get_articles_by_tag(tag_id))
        tag_name = get_tag(tag_id).tag_name
        return self.render("index.html", title=tag_name, data=data)


class ManageHandler(BaseHandler):
    def GET(self):
        @authentication
        def func():
            data = timeline_list()
            return self.render("editor.html", title="Manage", data=data)
        return func()


class RssHandler(BaseHandler):
    def GET(self):
        web.header('Content-type', "text/xml; charset=utf-8")
        data = markdown_to_html(list_all_articles())
        return render("rss.xml", title=self.NAME, data=data, url=web.ctx.host)


class SearchHandler(BaseHandler):
    def GET(self):
        return self.render("search.html", title='Search')

    def POST(self):
        v = web.input(kw='').kw
        if v:
            data = markdown_to_html(search_article(clean_input(v)))
            return self.render("index.html", title=self.NAME, data=data)
        else:
            return web.seeother('/search')



