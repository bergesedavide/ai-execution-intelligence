from app.database.engine import TestSessionLocal
from app.registry.model_repository import ModelRepository
from app.registry.model_service import ModelRegistryService
from app.schemas.model import ModelInfo
from app.database.models.model_registry import ModelRegistry


def test_model_registry_service():

    session = TestSessionLocal()

    try:
        repository = ModelRepository(session)
        service = ModelRegistryService(repository)

        model_info = ModelInfo(
            name="service-test-model",
            provider="test",
            capabilities=["chat"],
            context_window=4096,
            input_cost=0.0,
            output_cost=0.0,
            expected_quality=0.70,
            expected_latency_ms=250.0,
        )

        model = service.register_model(model_info)

        assert model.id is not None
        assert model.name == "service-test-model"

        retrieved_model = service.get_model(
            "service-test-model"
        )

        assert retrieved_model is not None
        assert retrieved_model.name == "service-test-model"

    finally:
        session.query(ModelRegistry).filter(
            ModelRegistry.name == "service-test-model"
        ).delete()

        session.commit()
        session.close()

def test_get_active_models():
    session = TestSessionLocal()

    try:
        repository = ModelRepository(session)
        service = ModelRegistryService(repository)

        model_info = ModelInfo(
            name="service-active-test-model",
            provider="test",
            capabilities=["chat"],
            context_window=8192,
            input_cost=0.0,
            output_cost=0.0,
            expected_quality=0.80,
            expected_latency_ms=200.0,
        )

        service.register_model(model_info)

        active_models = service.get_active_models()

        active_names = [
            model.name
            for model in active_models
        ]

        assert "service-active-test-model" in active_names

    finally:
            session.query(ModelRegistry).filter(
                ModelRegistry.name == "service-active-test-model"
            ).delete()

            session.commit()
            session.close()