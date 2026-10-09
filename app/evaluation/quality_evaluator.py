from ollama import Client

from app.schemas.quality_evaluation import QualityEvaluation


class QualityEvaluator:

    def __init__(
        self,
        client: Client,
        model: str,
    ):
        self.client = client
        self.model = model

    def evaluate(
        self,
        prompt: str,
        response: str,
    ) -> QualityEvaluation:

        result = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an impartial AI response evaluator. "
                        "Evaluate the quality of an AI-generated response "
                        "based on the original user prompt. "
                        "Score correctness, relevance, and completeness "
                        "from 0.0 to 1.0. "
                        "Calculate overall_score as the arithmetic mean "
                        "of the three scores. "
                        "Provide a concise explanation in reasoning. "
                        "Evaluate only the response, not the writing style. "
                        "Do not reward unsupported claims. "
                        "Return only valid JSON matching the requested schema."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Original prompt:\n{prompt}\n\n"
                        f"Generated response:\n{response}"
                    ),
                },
            ],
            format=QualityEvaluation.model_json_schema(),
        )

        return QualityEvaluation.model_validate_json(
            result["message"]["content"]
        )