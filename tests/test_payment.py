import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app 
from db.database import Base, SessionLocal
from models.models import Users, Transactions, Business
from routers.payment import get_db, get_current_user, get_all, get_business, get_transaction
from routers.auth import bcrypt_context
import random
import string

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

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

def test_create_transaction(client, db): 
    hashed_password = bcrypt_context.hash("hashedpassword")
    unique_username = f"testuser_{random_string()}"
    unique_email = f"test_{random_string()}@example.com"
    user = Users(email=unique_email, username=unique_username, hashed_password=hashed_password, is_active=True, role="user")
    db.add(user) 
    business = Business(name="Test Business", description="A test business")
    db.add(business)
    db.commit()

    app.dependency_overrides[get_current_user] = lambda: {"user_id": user.id, "user_role": "user"}

    response = client.post("/api/transaction", json={
        "business_id": business.id, 
        "card_number": "1234567890123456", 
        "card_type": 1, 
        "amount": 100.00, 
        "description": "Test transaction"
    })
    assert response.status_code == 200
    assert response.json()["amount"] == 100.00
