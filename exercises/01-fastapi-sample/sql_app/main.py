from typing import List

from fastapi import Depends, FastAPI, HTTPException, Header
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_session = Depends(get_db)


async def verify_key(x_api_token: str = Header(...), db: Session = db_session):
    db_user = crud.get_user_by_token(db, token=x_api_token)
    if db_user == None:
        raise HTTPException(status_code=400, detail="X-API-TOKEN header invalid")


@app.get("/health-check", dependencies=[Depends(verify_key)])
def health_check(db: Session = db_session):
    return {"status": "ok"}


@app.post("/users/", response_model=schemas.UserCreateResponse)
def create_user(user: schemas.UserCreate, db: Session = db_session):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User], dependencies=[Depends(verify_key)])
def read_users(skip: int = 0, limit: int = 100, db: Session = db_session):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, dependencies=[Depends(verify_key)])
def read_user(user_id: int, db: Session = db_session):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item, dependencies=[Depends(verify_key)])
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = db_session
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item], dependencies=[Depends(verify_key)])
def read_items(skip: int = 0, limit: int = 100, db: Session = db_session):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
