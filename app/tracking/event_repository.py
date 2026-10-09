from datetime import datetime

from sqlalchemy.orm import Session

from app.database.models.execution_event import ExecutionEvent


class EventRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_event(
        self,
        execution_id: int,
        event_type: str,
        timestamp: datetime,
    ) -> ExecutionEvent:
        event = ExecutionEvent(
            execution_id=execution_id,
            event_type=event_type,
            timestamp=timestamp,
        )

        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)

        return event