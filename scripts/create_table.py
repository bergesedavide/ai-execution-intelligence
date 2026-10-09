from app.database.base import Base
from app.database.engine import engine

from app.database.models.execution import Execution
from app.database.models.execution_event import ExecutionEvent
from app.database.models.model_registry import ModelRegistry
from app.database.models.quality_evaluation import QualityEvaluation


def create_tables():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()