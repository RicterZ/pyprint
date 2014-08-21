import tornado.web
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


class JinjaTemplateMixin(object):
    """A simple mixin of jinja2

    From: http://bibhas.in/blog/using-jinja2-as-the-template-engine-for-tornado-web-framework/
    """
    def jinja2_render(self, template_name, **kwargs):
        env = Environment(loader=FileSystemLoader(self.settings['template_path']))

        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        return template.render(settings=self.settings, **kwargs)


class BaseHandler(tornado.web.RequestHandler, JinjaTemplateMixin):
    @property
    def orm(self):
        return self.application.orm

    def render(self, template_name, **kwargs):
        """Override render method
        """
        self.write(self.jinja2_render(template_name, is_pjax=bool(self.request.headers.get('X-Pjax', None)),
                                      **kwargs))