import os.path
from hashlib import md5

# third-part
import tornado.web
from sqlalchemy.orm import scoped_session, sessionmaker

# custom
import views
from settings import *
from models import engine


theme_path = os.path.join(os.path.dirname(__file__), 'theme/{theme_name}'.format(theme_name=theme))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = views.handlers

        settings = dict(
            static_path=os.path.join(theme_path, 'static'),
            template_path=os.path.join(theme_path, 'templates'),

            username=username,
            email=email,
            email_md5=md5(email.lower()).hexdigest(),
            motto=motto,
            title=title,
            disqus_shortname=disqus_shortname,

            debug=debug,
        )

        tornado.web.Application.__init__(self, handlers=handlers, **settings)
        self.orm = scoped_session(sessionmaker(bind=engine))



