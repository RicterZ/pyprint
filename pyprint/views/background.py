import tornado.web
from datetime import date
from sqlalchemy.orm.exc import NoResultFound

from pyprint.handler import BaseHandler
from pyprint.models import User, Link, Post


class SignInHandler(BaseHandler):
    def get(self):
        return self.background_render('login.html')

    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        if username and password:
            try:
                user = self.orm.query(User).filter(User.username == username).one()
            except NoResultFound:
                return self.redirect('/login')
            if user.check(password):
                self.set_secure_cookie('username', user.username)
                self.redirect('/kamisama/posts')

        return self.redirect('/login')


class ManagePostHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        posts = self.orm.query(Post.title, Post.id).order_by(Post.id.desc()).all()
        self.background_render('posts.html', posts=posts)

    @tornado.web.authenticated
    def post(self):
        action = self.get_argument('action', None)
        if action == 'del':
            post_id = self.get_argument('id', 0)
            if post_id:
                post = self.orm.query(Post).filter(Post.id == post_id).one()
                self.orm.delete(post)
                self.orm.commit()


class AddPostHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.background_render('add_post.html', post=None)

    @tornado.web.authenticated
    def post(self):
        title = self.get_argument('title', None)
        content = self.get_argument('content', None)
        tags = self.get_argument('tags', '').strip().split(',')
        if not title or not content:
            return self.redirect('/kamisama/posts/add')

        post = self.orm.query(Post.title).filter(Post.title == title).all()
        if post:
            return self.write('<script>alert("Title has already existed");window.history.go(-1);</script>')
        self.orm.add(Post(title=title, content=content, created_time=date.today()))
        self.orm.commit()
        return self.redirect('/kamisama/posts')


class AddLinkHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        links = self.orm.query(Link).all()
        self.background_render('links.html', links=links)

    @tornado.web.authenticated
    def post(self):
        action = self.get_argument('action', None)
        if action == 'add':
            name = self.get_argument('name', '')
            url = self.get_argument('url', '')
            if not name or not url:
                return self.redirect('/kamisama/links')
            self.orm.add(Link(name=name, url=url))
            self.orm.commit()
            return self.redirect('/kamisama/links')

        elif action == 'del':
            link_id = self.get_argument('id', 0)
            if link_id:
                link = self.orm.query(Link).filter(Link.id == link_id).one()
                self.orm.delete(link)
                self.orm.commit()
