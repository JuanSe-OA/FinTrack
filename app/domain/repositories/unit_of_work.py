from abc import ABC, abstractmethod

from app.domain.repositories.alert_repository import AlertRepository
from app.domain.repositories.budget_repository import BudgetRepository
from app.domain.repositories.category_repository import CategoryRepository
from app.domain.repositories.transaction_repository import TransactionRepository
from app.domain.repositories.user_repository import UserRepository

class AbstractUnitOfWork(ABC):

    users: UserRepository
    transactions: TransactionRepository
    categories: CategoryRepository
    budgets: BudgetRepository
    alerts: AlertRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass
