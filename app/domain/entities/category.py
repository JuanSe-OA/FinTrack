from dataclasses import dataclass
from enum import Enum

from uuid import UUID

class CategoryType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


@dataclass
class Category:
    id: UUID
    user_id: UUID
    name: str
    type: CategoryType
    description: str | None = None

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError ("Ctageory name is required")