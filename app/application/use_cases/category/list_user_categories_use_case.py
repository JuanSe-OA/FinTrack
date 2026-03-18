from uuid import UUID

from app.application.unit_of_work import UnitOfWork
from app.domain.entities.category import Category


class ListUserCategoriesUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def execute(self, user_id: UUID) -> list[Category]:
        with self.uow:
            user = self.uow.users.get_by_id(user_id)
            if user is None:
                raise ValueError("User not found")
            
            if not user.is_active:
                raise PermissionError("User is not active")
            
            
            return self.uow.categories.get_all_by_user_id(user_id)
