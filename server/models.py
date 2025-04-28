from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, unique=True, index=True)
    name = Column(String)
    family = Column(String)
    password = Column(String)
    rule = Column(String)

class News(Base):
    __tablename__ = "news"
    news_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    image_url = Column(String)
    author = Column(String, ForeignKey("users.username"))  # تغییر ForeignKey
    date = Column(String)
    title = Column(String)
    summary = Column(String)
    body = Column(String)
