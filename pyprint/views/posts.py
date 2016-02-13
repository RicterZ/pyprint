#coding: utf-8
from itertools import groupby

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_
from pyprint.handler import BaseHandler
from pyprint.models import Post, Tag
from pyprint.utils import get_host
from pyprint import constants

from pyprint.settings import post_of_page


class ListPostsHandler(BaseHandler):
    def get(self, page=1):
        page = int(page) if int(page) else 1

        posts = self.orm.query(Post).filter(Post.type == constants.POST)\
            .order_by(Post.created_time.desc()).limit(post_of_page).offset(
            (page - 1) * post_of_page).all()

        return self.render('index.html', title=u'初心を忘れず', data={
            'preview': page - 1,
            'next': page + 1,
            'posts': posts
        })


class RetrievePostHandler(BaseHandler):
    def get(self, title):
        try:
            post = self.orm.query(Post).filter(and_(Post.title == title, Post.type == 'post')).one()
        except NoResultFound:
            return self.redirect('/akarin')

        return self.render('post.html', title=post.title, post=post)


class ListPostsByTagHandler(BaseHandler):
    def get(self, slug):
        try:
            tag = self.orm.query(Tag).filter(Tag.slug == slug).one()
        except NoResultFound:
            return self.redirect('/akarin')

        posts = [post for post in tag.posts if post.type == constants.POST]
        return self.render('index.html', title='Tag: %s' % tag.slug, data={
            'preview': 0,
            'next': 0,
            'posts': posts,
        })


class ArchiveHandler(BaseHandler):
    def get(self):
        posts = self.orm.query(Post.title, Post.created_time).\
            filter(Post.type == constants.POST).order_by(Post.created_time.desc()).all()

        posts_groups = [{'year': year, 'posts': list(posts)} for year, posts in
            groupby(posts, key=lambda p: p.created_time.year)]

        return self.render('archives.html', title='Archives', posts_groups=posts_groups)


class FeedHandler(BaseHandler):
    def get(self):
        posts = self.orm.query(Post).filter(Post.type == constants.POST).order_by(
            Post.created_time.desc()).limit(3).all()
        headers = {
            'Content-Type': 'application/xml',
        }
        return self.render('feed.xml', posts=posts,
                           url=get_host(self.request.full_url()), headers=headers)
