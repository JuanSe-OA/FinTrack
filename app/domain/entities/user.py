from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    email: str
    hashed_password: str
    is_active: bool
    created_at: datetime

    def __post_init__(self):
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email")
