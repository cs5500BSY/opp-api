from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app 
from db.database import Base
from models.models import Users, Transactions, Business
import pytest

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

def test_create_business(client):
    app.dependency_overrides[get_current_user] = lambda: {"user_id": 1, "user_role": "admin"}

    response = client.post("/api/business", json={"name": "Test Business", "description": "A test business"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Business"

def test_get_business(client, db):
    business = Business(name="Test Business", description="A test business")
    db.add(business)
    db.commit()

    response = client.get(f"/api/business/{business.id}")
    assert response.status_code == 200
    assert response.json()["id"] == business.id

def test_create_transaction(client):
    user = Users(email="test@example.com", username="testuser", hashed_password="hashedpassword", is_active=True, role="user")
    db.add(user)
    business = Business(name="Test Business", description="A test business")
    db.add(business)
    db.commit()

    app.dependency_overrides[get_current_user] = lambda: {"user_id": user.id, "user_role": "user"}

    response = client.post("/api/transaction", json={"business_id": business.id, "card_number": "1234567890123456", "card_type": 1, "amount": 100.00, "description": "Test transaction"})
    assert response.status_code == 200
    assert response.json()["amount"] == 100.00
