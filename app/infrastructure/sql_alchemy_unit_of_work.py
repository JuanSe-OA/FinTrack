from app.application.unit_of_work import UnitOfWork
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.repositories.sql_alchemy_alert_repository import SqlAlchemyAlertRepository
from app.infrastructure.repositories.sql_alchemy_budget_repository import SqlAlchemyBudgetRepository
from app.infrastructure.repositories.sql_alchemy_category_repository import SqlAlchemyCategoryRepository
from app.infrastructure.repositories.sql_alchemy_transaction_repository import SqlAlchemyTransactionRepository
from app.infrastructure.repositories.sql_alchemy_user_repository import SqlAlchemyUserRepository


class SqlAlchemyUnitOfWork(UnitOfWork):

    def __enter__(self):
        self.session = SessionLocal()

        self.users = SqlAlchemyUserRepository(self.session)
        self.transactions = SqlAlchemyTransactionRepository(self.session)
        self.categories = SqlAlchemyCategoryRepository(self.session)
        self.alerts = SqlAlchemyAlertRepository(self.session)
        self.budgets = SqlAlchemyBudgetRepository(self.session)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.rollback()
        else:
            self.commit()

        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
