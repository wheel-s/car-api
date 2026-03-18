import pytest
import warnings
from uuid import uuid4
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

    engine = create_engine( URL,connect_args={"check_same_thread":False} )
    testingSessionLocal = sessionmaker(autocommit=False,autoflush=False, bind = engine)
    
    Base.metadata.create_all(bind=engine)

    db = testingSessionLocal()


    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind= engine)


@pytest.fixture(scope="function")
def test_user():
    password_hash = get_password_hash("password123")
    return User(
        id=uuid4(),
        username = "faez",
        email = "test@example.com",
        password_hash = password_hash
    )


@pytest.fixture(scope="function")
def test_token_data():
    return TokenData(user_id=str(uuid4()))



@pytest.fixture(scope="function")
def auth_headers(client, db_session):
    response = client.post(
        "/auth/",
        data ={
            "email":"testuser@example.com",
            "password":"testpassword",
            "username":"User"

        }
    )
    assert response.status_code == 201
  



