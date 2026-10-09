import pytest
from ollama import Client
from unittest.mock import Mock

from app.database.engine import TestSessionLocal
from app.database.models.execution import Execution
from app.execution.execution_service import ExecutionService
from app.database.models.model_registry import ModelRegistry


def test_execution_service():

    client = Client(host="http://localhost:11435")
    session = TestSessionLocal()

    model = (
        session.query(ModelRegistry)
        .filter_by(name="llama3.1:8b")
        .one()
    )

    service = ExecutionService(
        client=client,
        session=session,
    )

    prompt = "Explain what a Python decorator is in one sentence."

    try:
        execution = service.create_execution(
            prompt=prompt,
            model_id=model.id,
            model_name="llama3.1:8b",
        )

        response = service.execute(execution)
        execution_id = execution.id

        assert execution_id is not None
        assert response
        assert isinstance(response, str)

        execution = (
            session.query(Execution)
            .filter(Execution.prompt == prompt)
            .order_by(Execution.id.desc())
            .first()
        )

        assert execution is not None
        assert execution.model_id == model.id
        assert execution.model_name == "llama3.1:8b"
        assert execution.status == "success"
        assert execution.latency_ms is not None
        assert execution.latency_ms > 0
        assert execution.input_tokens is not None
        assert execution.output_tokens is not None
        assert execution.completed_at is not None

    finally:
        if "execution" in locals() and execution is not None:
            session.delete(execution)
            session.commit()

        session.close()

def test_execution_service_handles_ollama_failure():
    client = Mock()
    client.chat.side_effect = RuntimeError("Simulated Ollama failure")

    session = Mock()

    execution = Execution(
        id=999,
        prompt="Test prompt",
        model_id=1,
        model_name="llama3.1:8b",
        started_at=__import__("datetime").datetime.now(
            __import__("datetime").UTC
        ),
        status="running",
    )

    service = ExecutionService(
        client=client,
        session=session,
    )

    with pytest.raises(RuntimeError, match="Simulated Ollama failure"):
        service.execute(execution)

    assert execution.status == "error"
    assert execution.completed_at is not None
    assert execution.latency_ms >= 0

    session.rollback.assert_called_once()
    session.commit.assert_called_once()

def test_execution_service_handles_commit_failure():
    client = Mock()
    client.chat.return_value = {
        "message": {"content": "Test response"},
        "prompt_eval_count": 10,
        "eval_count": 20,
    }

    session = Mock()
    session.commit.side_effect = [
        RuntimeError("Simulated database failure"),
        None,
    ]

    execution = Execution(
        id=1000,
        prompt="Test prompt",
        model_id=1,
        model_name="llama3.1:8b",
        started_at=__import__("datetime").datetime.now(
            __import__("datetime").UTC
        ),
        status="running",
    )

    service = ExecutionService(
        client=client,
        session=session,
    )

    with pytest.raises(RuntimeError, match="Simulated database failure"):
        service.execute(execution)

    assert execution.status == "error"
    assert execution.completed_at is not None

    assert session.rollback.call_count == 1
    assert session.commit.call_count == 2