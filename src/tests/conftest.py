import pytest
import warnings
from uuid import uuid4
from fastapi.testclient import TestClient
from src.main import app
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.core import Base
from src.entities.users import User
from src.entities.cars import Car, Brand
from src.auth.models import TokenData
from src.auth.service import get_password_hash
from src.rate_limiting import limiter


@pytest.fixture(scope="function")
def db_session():
    URL = "sqlite:///./test.db"

    engine = create_engine(URL, connect_args={"check_same_thread": False})
    testingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    db = testingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_user():
    password_hash = get_password_hash("password123")
    return User(
        id=uuid4(),
        username="faez",
        email="test@example.com",
        password_hash=password_hash,
    )


@pytest.fixture(scope="function")
def test_token_data():
    return TokenData(user_id=str(uuid4()))


@pytest.fixture(scope="function")
def client(db_session):
    from src.main import app
    from src.database.core import get_db

    limiter.reset()

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def auth_headers(client, db_session):
    response = client.post(
        "/auth/",
        json={
            "email": "testuser@example.com",
            "password": "testpassword",
            "username": "User",
        },
    )

    assert response.status_code == 201
    response = client.post(
        "/auth/token",
        data={
            "username": "testuser@example.com",
            "password": "testpassword",
            "grant_type": "password",
        },
    )

    assert response.status_code == 200
    data = response.json()
    token = data["access_token"]
    print(data)
    return {"Authorization": f"Bearer {token}"}
