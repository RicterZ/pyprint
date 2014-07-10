import json
from jinja2.environment import TemplateNotFound
from lib.utils import article_to_storage, markdown_to_html, json_format, datetime
from lib.http_response import HTTP_RESPONSE
from lib.authentication import authentication
from lib.models import *
from lib.settings import *


def response(status, message=""):
    def __json_of_date(obj):
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            raise TypeError('{obj} is not JSON serializable'.format(obj=obj))

    if status == 200:
        web.header('Content-Type', 'application/json')
        return json.dumps({"message": message}, default=__json_of_date)
    else:
        raise HTTP_RESPONSE[status]


class BaseHandler:
    def __init__(self):
        pass

    def render(self, template, **kwargs):
        return env.get_template(template).render(**kwargs)


class IndexHandler(BaseHandler):
    def GET(self):
        page = web.input(p=1).p
        try:
            page = int(page)
        except ValueError:
            page = 1
        page = 1 if page < 1 else page

        articles = web.ctx.orm.query(Article).order_by(Article.id.desc())[(page-1)*3:(page-1)*3+3]
        return self.render("index.html", data=articles, page=page)


class ArticleHandler(BaseHandler):
    def GET(self, article_id=None):
        if not article_id:
            return response(403)

        web_input = web.input(format='', raw='false')
        article = web.ctx.orm.query(Article).filter(Article.id == article_id).all()

        if len(article) == 0:
            return response(404)

        article = article if web_input.raw == 'true' else markdown_to_html(article)
        return response(200, json_format(article)) if web_input.format == 'json' \
            else self.render('index.html', data=article)

    def DELETE(self, article_id):
        #@authentication
        #def func():
        try:
            article = web.ctx.orm.query(Article).filter(Article.id == article_id).one()
            web.ctx.orm.delete(article)
            return response(204)
        except NoResultFound:
            return response(404)
        #return func()

    """def PUT(self, article_id):
        @authentication
        def func():
            data = web.input(title='', content='', tag='')
            if not (data.title == '' or data.content == ''):
                if update_a_article(article_id, data):
                    return response(200, "Update success")
                else:
                    return response(404)
        return func()"""

    def POST(self):
        #@authentication
        #def func():
        data = web.input(title='', content='', tags='')

        if not (data.title == '' or data.content == ''):
            add_tags = [Tag(name=tag) for tag in set(data.tags.split(','))
                        if tag and not web.ctx.orm.query(Tag).filter(Tag.name == tag).all()]
            map(web.ctx.orm.add, add_tags)
            tags = [web.ctx.orm.query(Tag).filter(Tag.name == tag)[0] for tag in set(data.tags.split(','))]
            article = Article(title=data.title, content=data.content, tags=tags)
            web.ctx.orm.add(article)
            return response(201)
        #return func()

"""
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
            return response(401, "Authentication failed")"""


class TimelineHandler(BaseHandler):
    def GET(self):
        return self.render("timeline.html", title="Timeline",
                           data=web.ctx.orm.query(Article.title, Article.date).all())

"""
class TagHandler(BaseHandler):
    def GET(self, tag_id):
        data = get_tag_for_articles(get_articles_by_tag(tag_id))
        tag_name = get_tag(tag_id).tag_name
        return self.render("index.html", title="Tag - " + tag_name, data=data)


class ManageHandler(BaseHandler):
    def GET(self):
        @authentication
        def func():
            data = timeline_list()
            return self.render("editor.html", title="", data=data)
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
            return self.render("settings.html", title="", data=data)
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
            data = get_friends_link()
            return self.render("links.html", title="", data=data)
        return func()

    def POST(self):
        @authentication
        def func():
            web_input = web.input(name='', link='', method='add', id=0)
            if web_input.method == 'add':
                if not web_input.name or not web_input.link:
                    return response(401)
                add_friend_link(web_input.name, web_input.link)
            elif web_input.method == 'delete':
                remove_friend_link(web_input.id)
            return web.seeother('/editor/friends')
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
"""