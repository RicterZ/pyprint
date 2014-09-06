import tornado.web

from pyprint.handler import BaseHandler
from pyprint.models import User, Link, Post


class SignInHandler(BaseHandler):
    def get(self):
        return self.render('login.html', title='Sign in')

    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        if username and password:
            user = self.orm.query(User).filter(User.username==username).one()
            if user.check(password):
                self.set_secure_cookie('username', user.username)
                self.redirect('/kamisama/posts')

        return self.redirect('/login')


class AddPostHandler(BaseHandler):
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

        elif action == 'add':
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