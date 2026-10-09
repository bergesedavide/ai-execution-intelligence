from app.schemas.prompt_analysis import (
    PromptAnalysis,
    PromptComplexity,
    PromptCategory,
)


def test_prompt_analysis():
    analysis = PromptAnalysis(
        category="coding",
        complexity="low",
        requires_reasoning=False,
        requires_tools=False,
        domain="programming",
        confidence=0.95,
    )

    assert analysis.category == PromptCategory.CODING
    assert analysis.complexity == PromptComplexity.LOW
    assert analysis.requires_reasoning is False
    assert analysis.requires_tools is False
    assert analysis.domain == "programming"
    assert 0.0 <= analysis.confidence <= 1.0