from dataclasses import dataclass
from uuid import UUID

from app.application.unit_of_work import UnitOfWork
from app.domain.entities.alert import Alert


class GetUserAlertsUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def execute(self, user_id: UUID) -> list[Alert]:
        with self.uow:
            user = self.uow.users.get_by_id(user_id)
            if user is None:
                raise ValueError("User not found")

            return self.uow.alerts.get_all_by_user_id(user_id)