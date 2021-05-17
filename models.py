from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
#from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Post(Base):
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    author_id = Column(Integer, ForeignKey('user.id'))

