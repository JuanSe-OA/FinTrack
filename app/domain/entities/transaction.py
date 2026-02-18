from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

@dataclass
class Transaction:
    id: UUID
    user_id: UUID
    category_id: UUID
    amount: Decimal
    created_at: datetime
    description: str | None = None

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
