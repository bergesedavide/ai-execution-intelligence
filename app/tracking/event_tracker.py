from datetime import UTC, datetime

from app.tracking.event_repository import EventRepository


class EventTracker:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    def track(
        self,
        execution_id: int,
        event_type: str,
    ):
        return self.repository.add_event(
            execution_id=execution_id,
            event_type=event_type,
            timestamp=datetime.now(UTC),
        )