import pytest
from unittest.mock import MagicMock

from app.evaluation.quality_evaluator import QualityEvaluator
from app.schemas.quality_evaluation import QualityEvaluation


def test_quality_evaluator():
    client = MagicMock()

    client.chat.return_value = {
        "message": {
            "content": """
            {
                "correctness": 0.9,
                "relevance": 1.0,
                "completeness": 0.8,
                "overall_score": 0.9,
                "reasoning": "The response is correct and relevant."
            }
            """
        }
    }

    evaluator = QualityEvaluator(
        client=client,
        model="llama3.1:8b",
    )

    result = evaluator.evaluate(
        prompt="What is Python?",
        response="Python is a high-level programming language.",
    )

    assert isinstance(result, QualityEvaluation)
    assert result.correctness == 0.9
    assert result.relevance == 1.0
    assert result.completeness == 0.8
    assert result.overall_score == 0.9
    assert result.reasoning == (
        "The response is correct and relevant."
    )

    client.chat.assert_called_once()

def test_quality_evaluator_invalid_json():
    client = MagicMock()

    client.chat.return_value = {
        "message": {
            "content": "This is not valid JSON"
        }
    }

    evaluator = QualityEvaluator(
        client=client,
        model="llama3.1:8b",
    )

    with pytest.raises(ValueError):
        evaluator.evaluate(
            prompt="What is Python?",
            response="Python is a programming language.",
        )