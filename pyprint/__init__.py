import os.path
from hashlib import md5

# third-part
import tornado.web
from sqlalchemy.orm import scoped_session, sessionmaker

# custom
import views
from settings import *
from models import engine


theme_path = os.path.join(os.path.dirname(__file__), 'themes/{theme_name}'.format(theme_name=theme))
background_path = os.path.join(os.path.dirname(__file__), 'background')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = views.handlers
        handlers.insert(0, (r'/kamisama/static/(.*)', tornado.web.StaticFileHandler,
                         {'path': os.path.join(background_path, 'static')}))

        settings = dict(
            background_template_path=os.path.join(background_path, 'templates'),

            static_path=os.path.join(theme_path, 'static'),
            template_path=os.path.join(theme_path, 'templates'),
            login_url='/login',
            cookie_secret=cookie_secret,

            post_of_page=post_of_page,

            username=username,
            email=email,
            email_md5=md5(email.lower()).hexdigest(),
            motto=motto,
            title=title,
            disqus_shortname=disqus_shortname,
            analytics_code=analytics_code,

            debug=debug,
        )


        tornado.web.Application.__init__(self, handlers=handlers, **settings)
        self.orm = scoped_session(sessionmaker(bind=engine))



