from dataclasses import dataclass
from decimal import Decimal
from sqlalchemy import UUID


@dataclass
class Budget:
    id: UUID
    user_id: UUID
    category_id: UUID
    month: int
    year: int
    limit_amount: Decimal

    def __post_init__(self):
        if self.limit_amount <= 0:
            raise ValueError("Budget must be positive")
