from app.database.engine import SessionLocal
from app.registry.model_repository import ModelRepository
from app.registry.model_service import ModelRegistryService
from app.schemas.model import ModelInfo
from app.database.models import Execution, ModelRegistry


def register_models():
    session = SessionLocal()

    try:
        repository = ModelRepository(session)
        service = ModelRegistryService(repository)

        llama = ModelInfo(
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
            expected_quality=0.80,
            expected_latency_ms=500.0,
        )

        service.register_model(llama)

        print("Model registered successfully:")
        print(f"- {llama.name}")

    finally:
        session.close()


if __name__ == "__main__":
    register_models()