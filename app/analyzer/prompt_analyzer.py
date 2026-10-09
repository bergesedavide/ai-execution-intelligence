import json
from ollama import Client

from app.schemas.prompt_analysis import PromptAnalysis


class PromptAnalyzer:

    def __init__(self, client: Client, model: str):
        self.client = client
        self.model = model

    def analyze(self, prompt: str) -> PromptAnalysis:

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI request analyzer. "
                        "Analyze the user's request and classify it. "
                        "Return valid JSON matching the provided schema. "
                        "The confidence field MUST be a decimal between "
                        "0.0 and 1.0, never a percentage. "
                        "For example, use 0.85 instead of 85."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            format=PromptAnalysis.model_json_schema(),
        )

        content = response["message"]["content"]
        data = json.loads(content)

        confidence = data.get("confidence")

        if isinstance(confidence, (int, float)) and not isinstance(
            confidence, bool
        ):
            if 1 < confidence <= 100:
                data["confidence"] = confidence / 100

        return PromptAnalysis.model_validate(data)