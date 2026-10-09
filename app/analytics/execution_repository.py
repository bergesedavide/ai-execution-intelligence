from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.execution import Execution


class ExecutionRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_execution(
        self,
        execution_id: int,
    ) -> Execution | None:

        statement = select(Execution).where(
            Execution.id == execution_id
        )

        return self.session.execute(
            statement
        ).scalar_one_or_none()

    def get_recent_executions(
        self,
        limit: int = 10,
    ) -> list[Execution]:

        statement = (
            select(Execution)
            .order_by(Execution.started_at.desc())
            .limit(limit)
        )

        return list(
            self.session.execute(statement)
            .scalars()
            .all()
        )

    def get_executions_by_model(
        self,
        model_name: str,
    ) -> list[Execution]:

        statement = (
            select(Execution)
            .where(
                Execution.model_name == model_name
            )
            .order_by(Execution.started_at.desc())
        )

        return list(
            self.session.execute(statement)
            .scalars()
            .all()
        )

    def get_successful_executions(
        self,
    ) -> list[Execution]:

        statement = (
            select(Execution)
            .where(
                Execution.status == "success"
            )
            .order_by(Execution.started_at.desc())
        )

        return list(
            self.session.execute(statement)
            .scalars()
            .all()
        )