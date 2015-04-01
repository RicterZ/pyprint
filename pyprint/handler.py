import tornado.web
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

import database
from utils import markdown, fix_lazy_load


class JinjaEnvironment(object):
    _flag = None
    _jinja_env = None
    _background_env = None

    def __new__(cls, *args, **kwargs):
        if not 'path' in kwargs:
            raise Exception('Path of FileSystemLoader required')

        if not cls._jinja_env and not kwargs['is_background']:
            cls._jinja_env = Environment(loader=FileSystemLoader(kwargs['path']))
        if not cls._background_env and kwargs['is_background']:
            cls._background_env = Environment(loader=FileSystemLoader(kwargs['path']))

        return cls._jinja_env if not kwargs['is_background'] else cls._background_env


class JinjaTemplateMixin(object):
    """A simple mixin of jinja2

    From: http://bibhas.in/blog/using-jinja2-as-the-template-engine-for-tornado-web-framework/
    """
    def _render(self, path, template_name, is_background=False, **kwargs):
        env = JinjaEnvironment(path=path, is_background=is_background)
        env.filters['markdown'] = markdown
        env.filters['fix_lazy_load'] = fix_lazy_load

        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        return template.render(settings=self.settings, **kwargs)

    def _jinja2_render(self, template_name, **kwargs):
        return self._render(self.settings['template_path'], template_name, **kwargs)

    def _background_render(self, template_name, **kwargs):
        return self._render(self.settings['background_template_path'], template_name,
                            is_background=True, **kwargs)


class BaseHandler(tornado.web.RequestHandler, JinjaTemplateMixin):
    @property
    def orm(self):
        return database.db()

    def on_finish(self):
        database.db.remove()

    def render(self, template_name, headers=None, **kwargs):
        """Override render method
        """
        if headers:
            for key, value in headers.iteritems():
                self.set_header(key, value)
        self.set_header('X-Zhazha', 'R1ct3r 1s zh@zh@')
        self.set_header('X-Powered-by', 'PyPrint')
        self.write(self._jinja2_render(template_name, is_pjax=bool(self.request.headers.get('X-Pjax', None)),
                                      **kwargs))
        self.finish()

    def background_render(self, template_name, **kwargs):
        self.write(self._background_render(template_name, **kwargs))
        self.finish()

    def get_current_user(self):
        return self.get_secure_cookie('username')
