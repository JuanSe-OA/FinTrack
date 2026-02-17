from dataclasses import dataclass
from enum import Enum

from sqlalchemy import UUID

class CategoryType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


@dataclass
class Category:
    id: UUID
    user_id: UUID
    name: str
    type: CategoryType
