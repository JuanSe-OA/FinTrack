from app.application.unit_of_work import UnitOfWork
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.repositories.user_repository import SqlAlchemyUserRepository


class SqlAlchemyUnitOfWork(UnitOfWork):

    def __enter__(self):
        self.session = SessionLocal()

        self.users = SqlAlchemyUserRepository(self.session)
        # luego agregaremos los demás repos

        return self

    def __exit__(self, *args):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
