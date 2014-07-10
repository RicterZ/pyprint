import web
import jinja2 as jj
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# database_type = 'mysql' or 'sqlite'
database_type = 'sqlite'
# these values is for mysql
MySQL_host = 'localhost'
MySQL_user = 'root'
MySQL_pass = ''
MySQL_DB = ''
# these values is for sqlite
sqlite_path = 'sqlite:///rixb1.db3'

# if you are a developer, you should set web.config.debug = True
web.config.debug = True

#from local_settings import *

if database_type == 'mysql':
    pass
elif database_type == 'sqlite':
    engine = create_engine(sqlite_path, echo=True)


def load_sqlalchemy(handler):
    web.ctx.orm = scoped_session(sessionmaker(bind=engine))

    try:
        return handler()
    except web.HTTPError:
        web.ctx.orm.commit()
        raise
    except Exception as e:
        web.ctx.orm.rollback()
        raise e
    finally:
        web.ctx.orm.commit()


env = jj.Environment(loader=jj.FileSystemLoader('templates'), autoescape=True)
