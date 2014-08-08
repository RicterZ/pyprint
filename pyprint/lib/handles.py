import web
from sqlalchemy.orm.exc import NoResultFound

from settings import config
from functions import render_template
from models import Post, Tag, Link


class BaseHandler(object):
    def render(self, template, title=None, is_pjax=False, **kwargs):
        return render_template(template, title=title if title else config['username'],
                               is_pjax=bool(web.ctx.env.get('HTTP_X_PJAX')), config=config, **kwargs)


class IndexHandler(BaseHandler):
    def GET(self, page=1):
        page = int(page) if page else 1
        posts = web.ctx.orm.query(Post).order_by(Post.id.desc())[(page - 1) * 3:3]

        return self.render('index.html', data={
            'preview': page - 1,
            'next': page + 1,
            'posts': posts,
        }, title='Index')


class PostHandler(BaseHandler):
    def GET(self, title):
        try:
            post = web.ctx.orm.query(Post).filter(Post.title == str(title).decode('utf-8')).one()
        except NoResultFound:
            return web.seeother('/akarin')

        return self.render('post.html', post=post, title='{title}'.format(title=title))


class TagHandler(BaseHandler):
    def GET(self, slug):
        tag = web.ctx.orm.query(Tag).filter(Tag.slug == slug).one()
        return self.render('index.html', data={
            'preview': 0,
            'next': 0,
            'posts': tag.posts,
        }, title='Tag - {slug}'.format(slug=slug))


class ArchivesHandler(BaseHandler):
    def GET(self):
        posts = web.ctx.orm.query(Post.title, Post.created_time).order_by(Post.id.desc()).all()

        posts_groups = []
        posts_group = None
        flag = None

        for i, post in enumerate(posts):
            year = post.created_time.year
            if not year == flag or flag is None:
                posts_group = {'year': year, 'posts_list': [post.title]}
            else:
                posts_group['posts_list'].append(post.title)

            if i == len(posts) - 1 or not posts_group in posts_groups:
                posts_groups.append(posts_group)
            flag = year

        return self.render('archives.html', posts_groups=posts_groups, title='Archives')


class LinkHandler(BaseHandler):
    def GET(self):
        links = web.ctx.orm.query(Link).all()
        return self.render('links.html', links=links, title='Links')


class NotFoundHandler(BaseHandler):
    def GET(self, url):
        return self.render('not_found.html', title='Akarin')


class FeedHandler(BaseHandler):
    def GET(self):
        posts = web.ctx.orm.query(Post).order_by(Post.id.desc())[0:3]
        return self.render('feed.xml', posts=posts, url=web.ctx.host)