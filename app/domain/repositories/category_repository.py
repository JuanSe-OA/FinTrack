from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.category import Category, CategoryType


class CategoryRepository(ABC):

    @abstractmethod
    def get_by_id(self, user_id: UUID, category_id: UUID) -> Category | None:
        pass


    @abstractmethod
    def get_by_name(self, name: str) -> Category | None:
        pass


    @abstractmethod
    def get_all_by_user_id(self, user_id: UUID) -> list[Category]:
        pass


    @abstractmethod
    def get_all_by_user_id_and_type(self, user_id: UUID, type: CategoryType) -> list[Category]:
        pass

    @abstractmethod
    def get_by_user_and_name(self, user_id: UUID, name: str) -> Category | None:
        pass


    @abstractmethod
    def add(self, category: Category) -> None:
        pass

    @abstractmethod
    def delete(self, category_id: UUID, user_id: UUID) -> None:
        pass