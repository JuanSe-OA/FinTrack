from dataclasses import dataclass
from uuid import UUID, uuid4
from app.application.unit_of_work import UnitOfWork
from app.domain.entities.category import Category, CategoryType


@dataclass
class CreateCategoryCommand:
    user_id: UUID
    name: str
    type : CategoryType
    description: str | None = None

class CreateCategoryUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def execute(self, cmd: CreateCategoryCommand) -> UUID:
        with self.uow:
            user = self.uow.users.get_by_id(cmd.user_id)
            if user is None:
                raise ValueError("User not found")
            
            if not user.is_active:
                raise PermissionError("User is not active")
            
            existing = self.uow.categories.get_by_user_and_name(cmd.user_id, cmd.name)
            if existing:
                raise ValueError("Category name already exists for this user")
            
            category = Category(
                id=uuid4(),
                user_id=cmd.user_id,
                name=cmd.name,
                type=cmd.type,
                description=cmd.description,
                
            )
            self.uow.categories.add(category)
            self.uow.commit()
            return category.id