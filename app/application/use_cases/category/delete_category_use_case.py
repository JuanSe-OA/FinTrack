from uuid import UUID

from app.application.unit_of_work import UnitOfWork


class DeleteCategoryUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def execute(self, category_id: UUID) -> None:
        with self.uow:
            category = self.uow.categories.get_by_id(category_id)
            if category is None:
                raise ValueError("Category not found")
            
            self.uow.categories.delete(category_id)
            self.uow.commit()
