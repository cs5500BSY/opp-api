from ..db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Double, TIMESTAMP, JSON, func


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    surname = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)


class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    business_id = Column(Integer, ForeignKey("business.id"))
    created_at = Column(TIMESTAMP, default=func.now())
    finished_at = Column(TIMESTAMP)
    type = Column(Integer) # 0 credit card, 1 debit card
    status = Column(String)
    amount = Column(Double)
    info = Column(JSON)


class Pending(Base):
    __tablename__ = 'pending'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    business_id = Column(Integer, ForeignKey("business.id"))
    created_at = Column(TIMESTAMP, default=func.now())
    wait_time = Column(Integer, default=2) # in days
    amount = Column(Double)
    info = Column(JSON)


class Business(Base):
    __tablename__ = 'business'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    credit = Column(Double, default=0.0)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=True)
    is_suspended = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
