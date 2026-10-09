from datetime import UTC, datetime
from time import perf_counter

from ollama import Client
from sqlalchemy.orm import Session

from app.database.models.execution import Execution


class ExecutionService:
    def __init__(self, client: Client, session: Session):
        self.client = client
        self.session = session

    def create_execution(
        self,
        prompt: str,
        model_id: int,
        model_name: str,
    ) -> Execution:
        execution = Execution(
            prompt=prompt,
            model_id=model_id,
            model_name=model_name,
            started_at=datetime.now(UTC),
            status="running",
        )

        self.session.add(execution)
        self.session.commit()
        self.session.refresh(execution)

        return execution

    def execute(self, execution: Execution) -> str:
        start_time = perf_counter()

        try:
            response = self.client.chat(
                model=execution.model_name,
                messages=[
                    {"role": "user", "content": execution.prompt}
                ],
            )

            content = response["message"]["content"]
            end_time = perf_counter()

            execution.completed_at = datetime.now(UTC)
            execution.latency_ms = (end_time - start_time) * 1000
            execution.input_tokens = response.get("prompt_eval_count", 0)
            execution.output_tokens = response.get("eval_count", 0)
            execution.status = "success"

            self.session.commit()
            self.session.refresh(execution)

            return content

        except Exception:
            end_time = perf_counter()

            self.session.rollback()

            execution.completed_at = datetime.now(UTC)
            execution.latency_ms = (end_time - start_time) * 1000
            execution.status = "error"

            try:
                self.session.commit()
            except Exception:
                self.session.rollback()

            raise

    def save(self, execution: Execution):
        self.session.commit()
        self.session.refresh(execution)

        return execution