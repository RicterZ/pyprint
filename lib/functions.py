import os

# third-party packages
from web import ctx, HTTPError
from sqlalchemy.orm import scoped_session, sessionmaker
from jinja2 import Environment, FileSystemLoader

# custom
from settings import templates
from models import engine


def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), templates)),
        extensions=extensions,
    )
    jinja_env.globals.update(globals)

    return jinja_env.get_template(template_name).render(context)


def load_sqlalchemy(handler):
    ctx.orm = scoped_session(sessionmaker(bind=engine))
    try:
        return handler()
    except HTTPError:
        ctx.orm.commit()
        raise
    except:
        ctx.orm.rollback()
        raise
    finally:
        ctx.orm.commit()