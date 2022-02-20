from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    hashed_pass_code = Column(String)
    pass_code_valid = Column(Boolean, default=True)
    
    alarms = relationship('Alarm', back_populates='owner')
    
class Alarm(Base):
    __tablename__ = 'alarms'

    id = Column(Integer, primary_key=True, index=True)
    alarm_name = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    
    owner = relationship('User', back_populates='alarms')
