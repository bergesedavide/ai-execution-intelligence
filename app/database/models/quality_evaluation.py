from datetime import UTC, datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class QualityEvaluation(Base):
    __tablename__ = "quality_evaluations"

    __table_args__ = (
        UniqueConstraint(
            "execution_id",
            name="uq_quality_evaluations_execution_id",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    execution_id: Mapped[int] = mapped_column(
        ForeignKey("executions.id"),
        nullable=False,
    )

    correctness: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    relevance: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    completeness: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    overall_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    reasoning: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    execution = relationship(
        "Execution",
        back_populates="quality_evaluation",
    )