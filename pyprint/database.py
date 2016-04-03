from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

from settings import connect_str


engine = create_engine(connect_str, echo=True, pool_recycle=3600)
Base = declarative_base()
db = scoped_session(sessionmaker(bind=engine))
