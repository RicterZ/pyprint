import json
import copy
from jinja2.environment import TemplateNotFound
from lib.utils import render, article_to_storage
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
        self.TITLE = data.blog_title
        self.NAME = data.username
        self.INTRO = data.blog_intro
        self.DISQUS = data.disqus_code
        self.EMAIL = data.email
        self.FRIENDS = get_friends_link()
        self.KEYWORD = data.blog_keyword
        self.DESCRIPTION = data.blog_description
        self.EMAIL_MD5 = password_to_md5(self.EMAIL.lower())

    def render(self, template, **kwargs):
        return render(template, NAME=self.NAME, EMAIL=self.EMAIL, FRIENDS=self.FRIENDS,
                      INTRO=self.INTRO, KEYWORD=self.KEYWORD, DESCRIPTION=self.DESCRIPTION,
                      EMAIL_MD5=self.EMAIL_MD5, **kwargs)


class IndexHandler(BaseHandler):
    def GET(self):
        page = web.input(p=1).p
        try:
            page = int(page)
        except ValueError:
            page = 1
        if page < 1:
            page = 1
        data = get_tag_for_articles(markdown_to_html(list_three_articles(page=page)))
        return self.render("index.html", title=self.TITLE, data=data, page=page)


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
            return self.render("editor.html", title="", data=data,
                               TITLE=self.TITLE, DISQUS=self.DISQUS)
        return func()

    def POST(self):
        @authentication
        def func():
            pass
        return func()


class SettingsHandler(BaseHandler):
    def GET(self):
        @authentication
        def func():
            data = timeline_list()
            return self.render("settings.html", title="", data=data,
                               TITLE=self.TITLE, DISQUS=self.DISQUS)
        return func()

    def POST(self):
        @authentication
        def func():
            data = web.input(
                username='', intro='', keyword='',
                desc='', main_title='', email='', disqus=''
            )
            save_settings(data)
            return web.seeother('/editor/settings')
        return func()


class RssHandler(object):
    def GET(self):
        web.header('Content-type', "text/xml; charset=utf-8")
        articles = markdown_to_html(list_three_articles())
        user_data = get_user_data()
        return render("rss.xml", title=user_data.username, articles=articles,
                      url=web.ctx.host, user_data=user_data, now=now())


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


class LinksHandler(BaseHandler):
    def GET(self):
        @authentication
        def func():
            return self.render("links.html", title="", TITLE=self.TITLE, DISQUS=self.DISQUS)
        return func()

    def POST(self):
        @authentication
        def func():
            web_input = web.input(name='', link='')
            if not web_input.name or not web_input.link:
                return response(400)
            add_friend_link(web_input.name, web_input.link)
            return response(200)
        return func()


class FriendHandler(BaseHandler):
    def GET(self):
        return self.render("friends.html", title="Friends",
                           DISQUS=self.DISQUS, friends=get_friends_link())


class PageHandler(object):
    def GET(self, page):
        try:
            template = env.get_template("pages/%s.html" % page)
        except TemplateNotFound:
            return response(404)
        return template.render()
