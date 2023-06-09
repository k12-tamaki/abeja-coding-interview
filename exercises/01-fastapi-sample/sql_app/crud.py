from sqlalchemy.orm import Session

from . import models, schemas

from secrets import token_hex


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_token(db: Session, token: str):
    return db.query(models.User).filter(models.User.token == token).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    token = token_hex(16) 
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, token=token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: schemas.User, skip: int = 0, limit: int = 100):
    db_user.is_active = False
    db.add(db_user)

    attach_db_user = db.query(models.User).filter(
        models.User.is_active == True and
        models.User.id != db_user.id
    ).order_by(models.User.id).first()
    if attach_db_user == None:
        return 'NotUser'
    atacch_items = db.query(models.Item).filter(models.Item.owner_id == db_user.id).offset(skip).limit(limit).all()
    for atacch_item in atacch_items:
        atacch_item.owner_id = attach_db_user.id
        db.add(atacch_item)

    db.commit()
    return 'OK'


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_items_by_me(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Item).filter(models.Item.owner_id == owner_id).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
