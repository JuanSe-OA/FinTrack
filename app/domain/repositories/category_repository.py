from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.category import Category


class CategoryRepository(ABC):

    @abstractmethod
    def get_by_id(self, category_id: UUID) -> Category | None:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Category | None:
        pass

    @abstractmethod
    def get_all_by_user_id(self, user_id: UUID) -> list[Category]:
        pass

    @abstractmethod
    def add(self, category: Category) -> None:
        pass