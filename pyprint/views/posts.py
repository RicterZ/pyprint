from sqlalchemy.orm.exc import NoResultFound
from pyprint.handler import BaseHandler
from pyprint.models import Post, Tag
from pyprint.utils import get_host


class ListPostsHandler(BaseHandler):
    def get(self, page=1):
        page = int(page)
        posts = self.orm.query(Post).order_by(Post.id.desc()).limit(3).offset((page - 1) * 3).all()

        return self.render('index.html', title='Index', data={
            'preview': page - 1,
            'next': page + 1,
            'posts': posts,
        })


class RetrievePostHandler(BaseHandler):
    def get(self, title):
        try:
            post = self.orm.query(Post).filter(Post.title == title).one()
        except NoResultFound:
            return self.redirect('/akarin')

        return self.render('post.html', title=post.title, post=post)


class ListPostsByTagHandler(BaseHandler):
    def get(self, slug):
        try:
            tag = self.orm.query(Tag).filter(Tag.slug == slug).one()
        except NoResultFound:
            return self.redirect('/akarin')

        return self.render('index.html', title='Tag: {slug}'.format(slug=slug), data={
            'preview': 0,
            'next': 0,
            'posts': tag.posts,
        })


class ArchiveHandler(BaseHandler):
    def get(self):
        posts = self.orm.query(Post.title, Post.created_time).order_by(Post.id.desc()).all()

        posts_groups = []
        posts_group = None
        flag = None

        for i, post in enumerate(posts):
            year = post.created_time.year
            if not year == flag or flag is None:
                posts_group = {'year': year, 'posts_list': [post.title]}
            else:
                posts_group['posts_list'].append(post.title)

            if (i == len(posts) - 1 and posts_group not in posts_groups) or \
                    not posts_group in posts_groups:
                posts_groups.append(posts_group)
            flag = year

        return self.render('archives.html', title='Archives', posts_groups=posts_groups)


class FeedHandler(BaseHandler):
    def get(self):
        posts = self.orm.query(Post).order_by(Post.id.desc()).limit(3)
        return self.render('feed.xml', posts=posts, url=get_host(self.request.full_url()))