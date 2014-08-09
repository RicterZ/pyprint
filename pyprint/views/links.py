from pyprint.handler import BaseHandler
from pyprint.models import Link


class ListLinksHandler(BaseHandler):
    def get(self):
        return self.render('links.html', links=self.orm.query(Link).all())