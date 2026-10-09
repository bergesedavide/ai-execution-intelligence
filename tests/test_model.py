from app.schemas.model import ModelInfo


def test_model_info():

    model = ModelInfo(
        name="llama3.1:8b",
        provider="ollama",
        capabilities=["coding", "chat", "reasoning"],
        context_window=128000,
        input_cost=0.0,
        output_cost=0.0,
        expected_quality=0.80,
        expected_latency_ms=500.0,
    )

    assert model.name == "llama3.1:8b"
    assert model.provider == "ollama"
    assert "coding" in model.capabilities
    assert model.context_window > 0
    assert model.input_cost >= 0
    assert model.output_cost >= 0
    assert 0.0 <= model.expected_quality <= 1.0
    assert model.expected_latency_ms > 0