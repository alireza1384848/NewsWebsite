from sqlalchemy.orm import Session
import models
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: models.User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_news(db: Session, news: models.News):
    db.add(news)
    db.commit()
    db.refresh(news)
    return news

def get_news_by_author(db: Session, author: str):
    return db.query(models.News).filter(models.News.author == author).all()

def get_news_by_id(db: Session, news_id: int):
    return db.query(models.News).filter(models.News.news_id == news_id).first()

def delete_news(db: Session, news: models.News):
    db.delete(news)
    db.commit()
def get_all_news(db: Session):
    return db.query(models.News).all()
