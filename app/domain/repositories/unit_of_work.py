from abc import ABC, abstractmethod

class AbstractUnitOfWork(ABC):

    users: any
    transactions: any
    categories: any
    budgets: any
    alerts: any

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
