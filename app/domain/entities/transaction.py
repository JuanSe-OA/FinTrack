from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class Transaction:
    id: UUID
    user_id: UUID
    category_id: UUID
    amount: float
    created_at: datetime
    description: str | None = None

    def validate(self):
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
