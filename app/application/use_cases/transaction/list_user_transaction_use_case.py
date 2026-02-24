from uuid import UUID

from app.application.unit_of_work import UnitOfWork
from app.domain.entities.transaction import Transaction 


class ListUserTransactionUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def execute(self, user_id: UUID) -> list[Transaction]:
        with self.uow:
            user = self.uow.users.get_by_id(user_id)
            if user is None:
                raise ValueError("User not found")
            
            return self.uow.transactions.list_by_user_id(user_id)
