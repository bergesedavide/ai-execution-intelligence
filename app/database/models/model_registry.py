from datetime import datetime, UTC

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ModelRegistry(Base):

    __tablename__ = "model_registry"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    capabilities: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
    )

    context_window: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    input_cost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    output_cost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    expected_quality: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    expected_latency_ms: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    execution = relationship(
        "Execution",
        back_populates="model",
    )