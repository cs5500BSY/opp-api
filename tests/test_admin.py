from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from db.database import Base
from models.models import Users
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

def test_read_all_users_as_admin(client):
    app.dependency_overrides[get_current_user] = lambda: {"user_role": "admin"}

    response = client.get("/admin/users")
    assert response.status_code == 200

def test_read_all_users_as_non_admin(client):
    app.dependency_overrides[get_current_user] = lambda: {"user_role": "user"}

    response = client.get("/admin/users")
    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication Failed"}

