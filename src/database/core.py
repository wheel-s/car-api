from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()


Database_URL = os.getenv("Database_URL")

engine = create_engine(Database_URL)

SessionLocal = sessionmaker(autoflush=True, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]
