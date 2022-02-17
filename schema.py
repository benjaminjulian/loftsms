from typing import Optional

from pydantic import BaseModel

class AlarmBase(BaseModel):
  alarm_name: str
  owner_id: int

class AlarmCreate(AlarmBase):
  pass

class Alarm(BaseModel):
  id: int

  owner_id: int
  
  class Config:
    orm_mode = True

class UserBase(BaseModel):
  phone_number: str
  pass_code_valid: bool
  
class UserCreate(UserBase):
  pass_code: str
  
class User(UserBase):
  id: int
  alarms: list[Alarm] = []
  
  class Config:
    orm_mode = True