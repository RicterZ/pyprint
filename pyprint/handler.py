import tornado.web
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

import database
from utils import markdown, fix_lazy_load


class JinjaTemplateMixin(object):
    """A simple mixin of jinja2

    From: http://bibhas.in/blog/using-jinja2-as-the-template-engine-for-tornado-web-framework/
    """
    def _render(self, _type, template_name, **kwargs):
        env = Environment(loader=FileSystemLoader(_type))
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
        return self._render(self.settings['background_template_path'], template_name, **kwargs)


class BaseHandler(tornado.web.RequestHandler, JinjaTemplateMixin):
    @property
    def orm(self):
        return database.db()

    def on_finish(self):
        database.db.remove()

    def render(self, template_name, headers={}, **kwargs):
        """Override render method
        """
        for key, value in headers.iteritems():
            self.set_header(key, value)
        self.set_header('X-JuJu', 'C3e_1s_j0j0')
        self.set_header('X-Powered-by', 'PyPrint')
        self.write(self._jinja2_render(template_name, is_pjax=bool(self.request.headers.get('X-Pjax', None)),
                                      **kwargs))

    def background_render(self, template_name, **kwargs):
        self.write(self._background_render(template_name, **kwargs))

    def get_current_user(self):
        return self.get_secure_cookie('username')
