from app.analytics.execution_repository import ExecutionRepository
from app.schemas.execution_analytics import ExecutionMetrics


class ExecutionAnalyticsService:

    def __init__(
        self,
        repository: ExecutionRepository,
    ):
        self.repository = repository

    def get_metrics(self) -> ExecutionMetrics:

        executions = (
            self.repository.get_recent_executions(
                limit=100000
            )
        )

        total_executions = len(executions)

        successful_executions = sum(
            execution.status == "success"
            for execution in executions
        )

        failed_executions = sum(
            execution.status == "error"
            for execution in executions
        )

        if total_executions == 0:
            return ExecutionMetrics(
                total_executions=0,
                successful_executions=0,
                failed_executions=0,
                success_rate=0.0,
                average_latency_ms=None,
                average_input_tokens=None,
                average_output_tokens=None,
            )

        success_rate = (
            successful_executions
            / total_executions
        )

        latencies = [
            execution.latency_ms
            for execution in executions
            if execution.latency_ms is not None
        ]

        input_tokens = [
            execution.input_tokens
            for execution in executions
            if execution.input_tokens is not None
        ]

        output_tokens = [
            execution.output_tokens
            for execution in executions
            if execution.output_tokens is not None
        ]

        average_latency_ms = (
            sum(latencies) / len(latencies)
            if latencies
            else None
        )

        average_input_tokens = (
            sum(input_tokens) / len(input_tokens)
            if input_tokens
            else None
        )

        average_output_tokens = (
            sum(output_tokens) / len(output_tokens)
            if output_tokens
            else None
        )

        return ExecutionMetrics(
            total_executions=total_executions,
            successful_executions=successful_executions,
            failed_executions=failed_executions,
            success_rate=success_rate,
            average_latency_ms=average_latency_ms,
            average_input_tokens=average_input_tokens,
            average_output_tokens=average_output_tokens,
        )