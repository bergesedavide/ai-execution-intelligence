import pytest

from app.database import models  # noqa: F401
from app.database.base import Base
from app.database.engine import TestSessionLocal, test_engine
from app.database.models.model_registry import ModelRegistry


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    if test_engine is None or TestSessionLocal is None:
        pytest.fail(
            "TEST_DATABASE_URL must be configured to run tests."
        )

    try:
        Base.metadata.create_all(bind=test_engine)

        session = TestSessionLocal()

        try:
            model = (
                session.query(ModelRegistry)
                .filter_by(name="llama3.1:8b")
                .first()
            )

            if model is None:
                model = ModelRegistry(
                    name="llama3.1:8b",
                    provider="ollama",
                    capabilities=[
                        "coding",
                        "chat",
                        "reasoning",
                        "summarization",
                    ],
                    context_window=128000,
                    input_cost=0.0,
                    output_cost=0.0,
                    expected_quality=0.8,
                    expected_latency_ms=500.0,
                )

                session.add(model)
                session.commit()

        finally:
            session.close()

        yield

    finally:
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session(setup_test_database):
    if TestSessionLocal is None:
        pytest.fail(
            "TEST_DATABASE_URL must be configured to run tests."
        )

    session = TestSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()