import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

test_engine = (
    create_engine(
        TEST_DATABASE_URL,
        pool_pre_ping=True,
    )
    if TEST_DATABASE_URL
    else None
)

TestSessionLocal = (
    sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )
    if test_engine
    else None
)
