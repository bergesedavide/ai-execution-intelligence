from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.quality_evaluation import QualityEvaluation as QualityEvaluationModel
from app.schemas.quality_evaluation import QualityEvaluation as QualityEvaluationSchema


class QualityRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(
        self,
        execution_id: int,
        evaluation: QualityEvaluationSchema,
    ) -> QualityEvaluationModel:

        quality_evaluation = QualityEvaluationModel(
            execution_id=execution_id,
            correctness=evaluation.correctness,
            relevance=evaluation.relevance,
            completeness=evaluation.completeness,
            overall_score=evaluation.overall_score,
            reasoning=evaluation.reasoning,
        )

        self.session.add(quality_evaluation)
        self.session.commit()
        self.session.refresh(quality_evaluation)

        return quality_evaluation

    def get_by_execution_id(
        self,
        execution_id: int,
    ) -> QualityEvaluationModel | None:

        statement = select(QualityEvaluationModel).where(
            QualityEvaluationModel.execution_id == execution_id
        )

        return self.session.execute(statement).scalar_one_or_none()