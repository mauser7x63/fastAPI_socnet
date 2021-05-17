from sqlalchemy.orm import Session
from models import User, Post
import schemas


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(email=user['key'], hashed_password=user['password'])
    print('ok')
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()


def create_user_post(db: Session, user_id: int, content: str):
    db_post = Post(author_id=user_id, content=content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts_by_user(db: Session, user_id: int):
    print('*'*50)
    print(db.query(Post).filter(Post.author_id == user_id).all())
    return db.query(Post).filter(Post.author_id == user_id).all()

def update_post(db:Session, post_id:int, like):
    db_post = db.query(Post).get(post_id)
    print(db_post)
    db_post.likes+=like
    print(db_post.likes)
    db.commit()
    db.refresh(db_post)
    return db_post