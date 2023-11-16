import responses
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from db.database import Base
from models.models import Users, Business
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

def setup_test_data(db):
    user = Users(email="test@example.com", username="testuser", hashed_password="hashedpassword", is_active=True, role="user")
    db.add(user)
    db.commit()

    business = Business(name="Test Business", description="A test business", is_verified=True)
    db.add(business)
    db.commit()

    return user, business

@responses.activate
def test_create_transaction_with_card_validation_and_fund_check(client, db):
    user, business = setup_test_data(db)

    # Mock the card validation API
    responses.add(
        responses.POST,
        "https://c3jkkrjnzlvl5lxof74vldwug40pxsqo.lambda-url.us-west-2.on.aws",
        json={"success": "true", "msg": "card number is valid."},
        status=200
    )

    responses.add(
        responses.POST,
        "https://223didiouo3hh4krxhm4n4gv7y0pfzxk.lambda-url.us-west-2.on.aws",
        json={"success": "true", "msg": "card number has sufficient funds and is not fraudulent"},
        status=200
    )

    response = client.post(
        "/api/transaction",
        json={
            "business_id": business.id, 
            "card_number": "4147202464191053",
            "card_type": 1,
            "amount": 100.00,
            "description": "Test transaction"
        }
    )

    assert response.status_code == 200

