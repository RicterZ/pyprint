#coding: utf-8
from sqlalchemy import create_engine, desc, or_
from sqlalchemy import Column, Table, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from settings import engine
from utils import today, password_to_md5


Base = declarative_base()
association_table = Table(
    'articles_tags', Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text)
    content = Column(Text)
    date = Column(DateTime, default=today())
    tags = relationship('Tag', secondary=association_table, backref='articles')

    def __repr__(self):
        return '<Post: {id}: {title}>'.format(id=self.id, title=self.title)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)

    def __repr__(self):
        return '<Tag: {id}: {name}>'.format(id=self.id, name=self.name)


class FriendLink(Base):
    __tablename__ = 'friend_links'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    link = Column(String)

    def __repr__(self):
        return '<Friend {name}: {link}>'.format(self.name, self.link)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    password = Column(String)

    def __init__(self, name, password):
        self.name = name
        self.password = password_to_md5(password)

    def check(self, password):
        return password_to_md5(password) == self.password

    def __repr__(self):
        return '<User: {name}>'.format(name=self.name)


#articles_table = Article.__tablename__
#tags_table = Tag.__tablename__
#friend_links_table = 'friend_links'
metadata = Base.metadata


if __name__ == '__main__':
    metadata.create_all(engine)

