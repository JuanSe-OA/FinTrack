from abc import abstractmethod, ABC
from uuid import UUID

from app.domain.entities.budget import Budget


class BudgetRepository(ABC):

    @abstractmethod
    def get_by_user_category_month_year(
        self,
        user_id: UUID,
        category_id: UUID,
        month: int,
        year: int
    ) -> Budget | None:
        pass

    @abstractmethod
    def add(self, budget: Budget) -> None:
        pass
    
    @abstractmethod
    def get_by_id(self, budget_id: UUID) -> None:
        pass


    @abstractmethod
    def update(self, budget: Budget) -> None:
        pass
