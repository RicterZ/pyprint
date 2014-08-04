import web
from sqlalchemy.orm.exc import NoResultFound
from settings import config
from functions import render_template
from models import Post, Tag, Link


class BaseHandler(object):
    def render(self, template, title=None, is_pjax=False, **kwargs):
        return render_template(template, title=title if title else config['username'],
                               is_pjax=bool(web.ctx.env.get('HTTP_X_PJAX')), config=config, **kwargs)


class TestHandler(BaseHandler):
    def GET(self):
        return 'Hi'


class IndexHandler(BaseHandler):
    def GET(self):
        input_data = web.input(page=0)
        posts = web.ctx.orm.query(Post).order_by(Post.created_time)[int(input_data.page) * 3 : 3]
        return self.render('index.html', posts=posts)


class PostHandler(BaseHandler):
    def GET(self, title):
        try:
            post = web.ctx.orm.query(Post).filter(Post.title == title).one()
        except NoResultFound:
            return web.seeother('/akarin')

        return self.render('post.html', post=post, title='{title}'.format(title=title))


class TagHandler(BaseHandler):
    def GET(self, slug):
        tag = web.ctx.orm.query(Tag).filter(Tag.slug == slug).one()
        return self.render('post.html', posts=tag.posts, title='Tag - {slug}'.format(slug=slug))


class LinkHandler(BaseHandler):
    def GET(self):
        links = web.ctx.orm.query(Link).all()
        return self.render('link.html', links=links, title='Links')


class NotFoundHandler(BaseHandler):
    def GET(self, url):
        return self.render('not_found.html', title='Akarin')

