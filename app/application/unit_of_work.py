from abc import ABC, abstractmethod
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.category_repository import CategoryRepository
from app.domain.repositories.transaction_repository import TransactionRepository
from app.domain.repositories.budget_repository import BudgetRepository
from app.domain.repositories.alert_repository import AlertRepository


class UnitOfWork(ABC):

    users: UserRepository
    categories: CategoryRepository
    transactions: TransactionRepository
    budgets: BudgetRepository
    alerts: AlertRepository

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, *args):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass
