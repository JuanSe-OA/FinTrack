from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import UUID


@dataclass
class User:
    id: UUID
    email: str
    hashed_password: str
    is_active: bool
    created_at: datetime
