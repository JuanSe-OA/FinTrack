from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.transaction import Transaction
from app.domain.entities.user import User

class TransactionRepository (ABC):

    @abstractmethod
    def add(self, transaction: Transaction ) -> None:
        pass

    @abstractmethod
    def get_by_id(self, transaction_id) -> Transaction | None:
        pass

    @abstractmethod
    def list_by_user_id(self, user_id) -> list[User]:
        pass

    @abstractmethod
    def get_total_expenses_for_month(
        self,
        user_id : UUID,
        category_id: UUID,
        year: int,
        month: int
    )-> float:
        pass