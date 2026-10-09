from datetime import datetime

from pydantic import BaseModel


class ExecutionEvent(BaseModel):
    execution_id: int
    event_type: str
    timestamp: datetime