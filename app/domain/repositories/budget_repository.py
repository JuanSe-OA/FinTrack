from abc import abstractmethod, ABC
from uuid import UUID

from app.domain.entities.budget import Budget


class BudgetRepository(ABC):

    @abstractmethod
    def get_by_user_category_month(
        self,
        user_id: UUID,
        category_id: UUID,
        year: int,
        month: int
    ) -> Budget | None:
        pass

    @abstractmethod
    def add(self, budget: Budget) -> None:
        pass
