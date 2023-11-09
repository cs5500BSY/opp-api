from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Depends, Path, HTTPException, Query
from pydantic import BaseModel, Field
from starlette import status
from sqlalchemy import cast, Date
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from routers.auth import get_current_user
from routers.helpers import check_user_authentication

from models.models import Transactions, Users, Business, Pending
from db.database import SessionLocal

router = APIRouter(prefix='/api')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

# when an API uses this, it will enforce authorization
user_dependency = Annotated[dict, (Depends(get_current_user))]


class CreateTransactionRequest(BaseModel):
    business_id: int
    card_number: str
    card_type: int
    amount: float
    description: str

@router.get("/transactions")
async def get_all(
    user: user_dependency,
    db: db_dependency,
    start_date: datetime = Query(default=None, alias="start_time"),  # Using an alias for clarity
    end_date: datetime = Query(default=None, alias="end_time")  # Using an alias for clarity
):
    check_user_authentication(user)

    # We start with a base query
    query = db.query(Transactions).filter(Transactions.user_id == user.get('id'))

    # If a start date is provided, filter records from that date onwards
    if start_date:
        query = query.filter(cast(Transactions.created_at, Date) >= start_date.date())

    # If an end date is provided, filter records up to that date
    if end_date:
        # The following ensures the end_date is inclusive by taking the entire day into account
        end_of_day = datetime.combine(end_date.date(), datetime.max.time())
        query = query.filter(cast(Transactions.created_at, Date) <= end_of_day.date())

    # Execute the query and return the results
    return query.all()
    
@router.get("/transaction/{transaction_id}")
async def get_transaction(user: user_dependency, db: db_dependency, transaction_id: int = Path(gt=0)):
    check_user_authentication(user)
    transaction = db.query(Transactions).filter(Transactions.id == transaction_id).filter(Transactions.user_id == user.get('id')).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail='Transaction not found')
    return transaction

@router.post("/transaction")
async def create_transaction(user: user_dependency, db: db_dependency, transaction_request: CreateTransactionRequest):
    check_user_authentication(user)
    business = db.query(Business).filter(Business.id == transaction_request.business_id).first()
    if business is None:
        raise HTTPException(status_code=404, detail='Business not found')
    if business.is_suspended:
        raise HTTPException(status_code=403, detail='Business is suspended')
    if business.is_deleted:
        raise HTTPException(status_code=403, detail='Business is deleted')
    if not business.is_verified:
        raise HTTPException(status_code=403, detail='Business is not verified')
    
    # TODO validate card number

    # TODO add locking
    # When multiple transactions are trying to update the business.credit at the same time, you could run into race conditions where some updates are lost because they are overwritten by others that read the old value before the update was committed.

    try:
        # if using credit card
        if transaction_request.card_type == 0:
            pending = Pending(user_id=user.get('id'), business_id=transaction_request.business_id, amount=transaction_request.amount, info={'card_number': '***' + transaction_request.card_number[-4:], 'description': transaction_request.description})
            db.add(pending)
            db.commit()
            db.refresh(pending)
            return pending
        
        # if using debit card
        if transaction_request.card_type == 1:
            transaction = Transactions(user_id=user.get('id'), business_id=transaction_request.business_id, type=transaction_request.card_type, status='completed', amount=transaction_request.amount, info={'card_number': '***' + transaction_request.card_number[-4:], 'card_type': transaction_request.card_type, 'description': transaction_request.description})
            db.add(transaction)
            # update business credit
            business.credit += transaction_request.amount
            db.commit()
            db.refresh(transaction)
            return transaction
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


class CreateBusinessRequest(BaseModel):
    name: str
    description: str

@router.post("/business")
async def create_business(user: user_dependency, db: db_dependency, business_request: CreateBusinessRequest):
    check_user_authentication(user)
    business = Business(name=business_request.name, description=business_request.description)
    db.add(business)
    db.commit()
    db.refresh(business)
    return business


@router.get("/business/{business_id}")
async def get_business(user: user_dependency, db: db_dependency, business_id: int = Path(gt=0)):
    check_user_authentication(user)
    business = db.query(Business).filter(Business.id == business_id).first()
    if business is None:
        raise HTTPException(status_code=404, detail='Business not found')
    if business.is_suspended:
        raise HTTPException(status_code=403, detail='Business is suspended')
    if business.is_deleted:
        raise HTTPException(status_code=403, detail='Business is deleted')
    if not business.is_verified:
        raise HTTPException(status_code=403, detail='Business is not verified')
    return business


@router.put("/business/{business_id}")
async def update_business(user: user_dependency, db: db_dependency, business_id: int = Path(gt=0), business_request: CreateBusinessRequest = None):
    check_user_authentication(user)
    business = db.query(Business).filter(Business.id == business_id).first()
    if business is None:
        raise HTTPException(status_code=404, detail='Business not found')
    if business.is_suspended:
        raise HTTPException(status_code=403, detail='Business is suspended')
    if business.is_deleted:
        raise HTTPException(status_code=403, detail='Business is deleted')
    if not business.is_verified:
        raise HTTPException(status_code=403, detail='Business is not verified')
    if business_request is not None:
        business.name = business_request.name
        business.description = business_request.description
        db.commit()
    return business


@router.delete("/business/{business_id}")
async def delete_business(user: user_dependency, db: db_dependency, business_id: int = Path(gt=0)):
    check_user_authentication(user)
    business = db.query(Business).filter(Business.id == business_id).first()
    if business is None:
        raise HTTPException(status_code=404, detail='Business not found')
    if business.is_suspended:
        raise HTTPException(status_code=403, detail='Business is suspended')
    if business.is_deleted:
        raise HTTPException(status_code=403, detail='Business is deleted')
    if not business.is_verified:
        raise HTTPException(status_code=403, detail='Business is not verified')
    business.is_deleted = True
    db.commit()
    return business

