from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from main import app
from routers.auth import get_db, bcrypt_context
from db.database import Base
from models.models import Users
import pytest
import random
import string

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()

    session = scoped_session(SessionLocal, scopefunc=lambda: 0)
    session.bind = connection

    Base.metadata.create_all(bind=engine)

    yield session

    session.remove()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

def random_string(length=6):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def test_signup(client: TestClient):
    unique_email = f"test_{random_string()}@example.com"
    unique_username = f"testuser_{random_string()}"
    response = client.post("/api/signup", json={
        "email": unique_email, 
        "password": "password123", 
        "username": unique_username
    })
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"

def test_login(client: TestClient, db):
    hashed_password = bcrypt_context.hash("hashedpassword")
    user = Users(
        email="testlogin@example.com",
        username="testlogin",
        hashed_password=hashed_password,
        is_active=True,
        role="user"
    )
    db.add(user)
    db.commit()

    response = client.post("/api/login", json={
        "email": "testlogin@example.com",
        "password": "hashedpassword"
    })
    print(response.json())  
    assert response.status_code == 200




