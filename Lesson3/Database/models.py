from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import time

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
)

Base = declarative_base()

tag_post = Table(
    'tag_post',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('post.id')),
    Column('tag_id', Integer, ForeignKey('tag.id')),
) # блок к дз №3. Связь - многое ко многому

class Post(Base):
    __tablename__ = 'post'
    id = Column('column', Integer, primary_key=True, autoincrement=True)
    url = Column(String(2048), unique=True, nullable=False)
    title = Column(String, nullable=False, unique=False)
    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)
    author = relationship('Author', backref='posts')
    tags = relationship('Tag', secondary=tag_post, backref='posts') # строка к дз №3. доп таблица для связи

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(2048), unique=True, nullable=False)
    name = Column(String, nullable=False, unique=False)
    gb_id = Column(Integer, nullable=True, unique=True) # строка к дз №3

# отсюда всё к дз №3

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(2048), nullable=False, unique=True)
    name = Column(String(150), nullable=False)

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('comment.id'), nullable=True)
    likes_count = Column(Integer, ForeignKey('comment.id'), nullable=True)
    body = Column(String)
    created_at = Column(DataTime, nullable=False)
    hidden = Column(Boolean)
    deep = Column(Integer)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship('Author', backref='comments')
    time_now = Column(DataTime)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship(Post, backref='comments')

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.parent_id = kwargs['parent_id']
        self.likes_count = kwargs['likes_count']
        self.body = kwargs['body']
        self.created_at = dt.datetime.fromisoformat(kwargs['created_at'])
        self.hidden = kwargs['hidden']
        self.deep = kwargs['deep']
        self.time_now = dt.datetime.fromisoformat(kwargs['time_now'])
