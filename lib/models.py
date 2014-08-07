from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey, Date
from sqlalchemy.orm import relationship


engine = create_engine('sqlite:///sqlite.db', echo=True)
Base = declarative_base()


posts_tags = Table('posts_tags', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')),
)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(50), unique=True, nullable=False)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)
    tags = relationship('Tag', secondary=posts_tags, backref='posts')
    created_time = Column(Date, default=date.today())
    content = Column(Text)


class Link(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    url = Column(String)


metadata = Base.metadata

if __name__ == "__main__":
    metadata.create_all(engine)
