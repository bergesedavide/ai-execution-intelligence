from datetime import datetime, UTC

from sqlalchemy import DateTime, Float, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Execution(Base):

    __tablename__ = "executions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    model_id: Mapped[int] = mapped_column(
        ForeignKey("model_registry.id"),
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    latency_ms: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    input_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    output_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    input_cost: Mapped[int | None] = mapped_column(
        Float,
        nullable=True,
    )

    output_cost: Mapped[int | None] = mapped_column(
        Float,
        nullable=True,
    )

    total_cost: Mapped[int | None] = mapped_column(
        Float,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    model = relationship(
        "ModelRegistry",
        back_populates="execution",
    )

    events = relationship(
        "ExecutionEvent",
        back_populates="execution",
        cascade="all, delete-orphan",
    )

    quality_evaluation = relationship(
        "QualityEvaluation",
        back_populates="execution",
        uselist=False,
        cascade="all, delete-orphan",
    )