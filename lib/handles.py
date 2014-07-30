import web
from sqlalchemy.orm.exc import NoResultFound
from settings import config
from functions import render_template
from models import Post


class BaseHandler(object):

    def render(self, template, title=None, is_pjax=False, **kwargs):
        return render_template(template, title=title if title else config['username'],
                               is_pjax=bool(web.ctx.env.get('HTTP_X_PJAX')), config=config, **kwargs)


class IndexHandler(BaseHandler):
    def GET(self):
        input_data = web.input(page=0)
        posts = web.ctx.orm.query(Post).order_by(Post.id)[int(input_data.page) * 3 : 3]
        return self.render('index.html', posts=posts)


class PostHandler(BaseHandler):
    def GET(self, post_id):
        try:
            post = web.ctx.orm.query(Post).filter(Post.id == post_id).one()
        except NoResultFound:
            return web.seeother('/akarin')

        return self.render('post.html', post=post)