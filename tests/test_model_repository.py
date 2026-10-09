from app.database.engine import TestSessionLocal
from app.registry.model_repository import ModelRepository
from app.schemas.model import ModelInfo
from app.database.models.model_registry import ModelRegistry


def test_model_repository():

    session = TestSessionLocal()

    try:
        repository = ModelRepository(session)

        model_info = ModelInfo(
            name="test-model",
            provider="test",
            capabilities=["chat", "reasoning"],
            context_window=8192,
            input_cost=0.0,
            output_cost=0.0,
            expected_quality=0.75,
            expected_latency_ms=300.0,
        )

        model = repository.add_model(model_info)

        assert model.id is not None
        assert model.name == "test-model"
        assert model.provider == "test"
        assert model.capabilities == ["chat", "reasoning"]

        retrieved_model = repository.get_model("test-model")

        assert retrieved_model is not None
        assert retrieved_model.id == model.id

    finally:
        session.query(ModelRegistry).filter(
            ModelRegistry.name == "test-model"
        ).delete()

        session.commit()
        session.close()

def test_get_active_models():
    session = TestSessionLocal()

    try:
        repository = ModelRepository(session)

        active_model_info = ModelInfo(
            name="active-test-model",
            provider="test",
            capabilities=["chat"],
            context_window=8192,
            input_cost=0.0,
            output_cost=0.0,
            expected_quality=0.80,
            expected_latency_ms=200.0,
        )

        inactive_model_info = ModelInfo(
            name="inactive-test-model",
            provider="test",
            capabilities=["chat"],
            context_window=8192,
            input_cost=0.0,
            output_cost=0.0,
            expected_quality=0.80,
            expected_latency_ms=200.0,
        )

        active_model = repository.add_model(active_model_info)
        inactive_model = repository.add_model(inactive_model_info)

        inactive_model.is_active = False
        session.commit()

        active_models = repository.get_active_models()

        active_names = [
            model.name
            for model in active_models
        ]

        assert active_model.name in active_names
        assert inactive_model.name not in active_names

    finally:
        session.query(ModelRegistry).filter(
            ModelRegistry.name == "active-test-model"
        ).delete()

        session.query(ModelRegistry).filter(
            ModelRegistry.name == "inactive-test-model"
        ).delete()

        session.commit()
        session.close()