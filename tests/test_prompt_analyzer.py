from ollama import Client

from app.analyzer.prompt_analyzer import PromptAnalyzer
from app.schemas.prompt_analysis import PromptAnalysis


def test_prompt_analyzer():

    client = Client(host="http://localhost:11435")

    analyzer = PromptAnalyzer(
        client=client,
        model="llama3.1:8b",
    )

    analysis = analyzer.analyze(
        "Write a Python function that reads a CSV file and calculates the average."
    )

    assert isinstance(analysis, PromptAnalysis)

    assert analysis.category
    assert analysis.complexity
    assert isinstance(analysis.requires_reasoning, bool)
    assert isinstance(analysis.requires_tools, bool)
    assert analysis.domain
    assert 0.0 <= analysis.confidence <= 1.0