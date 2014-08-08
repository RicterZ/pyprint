import os

# third-party packages
from web import ctx, HTTPError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from jinja2 import Environment, FileSystemLoader

# custom
from settings import templates, db_config


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


def get_connect_str(db_type, db_user, db_pass, db_name, host='localhost', port=3306):
    if db_type == 'sqlite':
        return 'sqlite:///{db_name}'.format(db_name=db_name)

    if db_type == 'mysql':
        return 'mysql:///{db_user}:{db_pass}@{host}:{port}/{db_name}'\
            .format(db_user=db_user, db_pass=db_pass,
                    db_name=db_name, port=port, host=host)

engine = create_engine(get_connect_str(**db_config), echo=True)
