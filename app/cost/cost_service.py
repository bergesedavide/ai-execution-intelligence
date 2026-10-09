from app.database.models.execution import Execution
from app.database.models.model_registry import ModelRegistry
from app.schemas.execution_cost import ExecutionCost


class CostService:
    def calculate(
        self,
        execution: Execution,
        model: ModelRegistry,
    ) -> ExecutionCost:

        input_tokens = execution.input_tokens or 0
        output_tokens = execution.output_tokens or 0

        input_cost = (
            input_tokens * model.input_cost
        )

        output_cost = (
            output_tokens * model.output_cost
        )

        total_cost = input_cost + output_cost

        return ExecutionCost(
            input_cost=input_cost,
            output_cost=output_cost,
            total_cost=total_cost,
        )