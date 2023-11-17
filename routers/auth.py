from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from starlette import status

from models.models import Users
from passlib.context import CryptContext
from db.database import SessionLocal
from typing import Annotated, Any
from sqlalchemy.orm import Session
from jose import jwt, JWTError

router = APIRouter(prefix='/api', tags=['auth'])

import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# These are used to create the signature for a JWT
SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cd63b88e8d3e7'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class CreateUserRequest(BaseModel):
    email: str
    password: str
    username: str = None  # Make username optional and default to None
    role: str = 'user'  # Default role to 'user'

    def __init__(self, **data):
        super().__init__(**data)
        self.username = self.username or self.email

class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    # Check if the email is already in use
    existing_user = db.query(Users).filter(Users.email == create_user_request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )

    # username defaults to email if not provided in the CreateUserRequest
    username = create_user_request.username if create_user_request.username else create_user_request.email
    # role defaults to 'user' if not provided in the CreateUserRequest
    role = create_user_request.role if create_user_request.role else 'user'

    create_user_model = Users(
        email=create_user_request.email,
        username=username,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        role=role
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {'message': 'User created successfully', 'user_id': create_user_model.id}



@router.post("/login", response_model=Token)
async def login_for_access_token(login_request: LoginRequest,
db: db_dependency):
    # Authenticate the user
    # TODO: check if form_data is validated by FastAPI
    user = authenticate_user(login_request.email, login_request.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    # Create token from the authenticated user
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=30))

    return {'access_token': token, 'token_type': 'bearer'}


def authenticate_user(email: str, password: str, db: db_dependency) -> Any:
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    claims = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.utcnow() + expires_delta
    claims.update({'exp': expires})
    token = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)
    return token


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
