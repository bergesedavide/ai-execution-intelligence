from datetime import datetime, UTC

from app.database.engine import SessionLocal
from app.database.models.execution import Execution
from app.database.models.model_registry import ModelRegistry


def test_execution_model():

    session = SessionLocal()

    model = (
        session.query(ModelRegistry)
        .filter_by(name="llama3.1:8b")
        .one()
    )

    execution = Execution(
        prompt="Explain how Python decorators work.",
        model_id=model.id,
        model_name="llama3.1:8b",
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
        latency_ms=450.0,
        input_tokens=20,
        output_tokens=100,
        status="success",
    )

    try:
        session.add(execution)
        session.commit()
        session.refresh(execution)

        assert execution.id is not None
        assert execution.prompt == (
            "Explain how Python decorators work."
        )
        assert execution.model_name == "llama3.1:8b"
        assert execution.latency_ms == 450.0
        assert execution.input_tokens == 20
        assert execution.output_tokens == 100
        assert execution.status == "success"

    finally:
        session.delete(execution)
        session.commit()
        session.close()