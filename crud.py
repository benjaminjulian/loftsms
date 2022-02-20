from sqlalchemy.orm import Session

import models
import schemas

def get_user(db: Session, user_id: int):
  return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_phone(db: Session, phone_number: str):
  return db.query(models.User).filter(models.User.phone_number == phone_number).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
  fake_hashed_pass_code = str(user.pass_code) + "ABCD"
  db_user = models.User(phone_number=user.phone_number, hashed_pass_code=fake_hashed_pass_code, pass_code_valid=True)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user
