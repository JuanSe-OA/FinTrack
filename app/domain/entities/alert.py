from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import UUID


@dataclass
class Alert:
    id: UUID
    user_id: UUID
    message: str
    created_at: datetime
    read: bool = False
