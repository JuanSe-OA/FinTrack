from dataclasses import dataclass
from sqlalchemy import UUID


@dataclass
class Budget:
    id: UUID
    user_id: UUID
    category_id: UUID
    month: int
    year: int
    limit_amount: float

    def validate(self):
        if self.limit_amount <= 0:
            raise ValueError("Budget must be positive")
