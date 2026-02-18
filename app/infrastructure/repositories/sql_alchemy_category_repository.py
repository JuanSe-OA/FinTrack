from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.category import Category
from app.domain.repositories.category_repository import CategoryRepository
from app.infrastructure.database.models.category_model import CategoryModel


class SqlAlchemyCategoryRepository(CategoryRepository):
    def __init__(self, session: Session):
        self.session = session
        

    def get_by_id(self, category_id: UUID) -> Category | None:
        model = self.session.get(CategoryModel, category_id)
        if not model:
            return None
        return Category (
            id=model.id,
            name=model.name,
            user_id=model.user_id,
            type= model.type,
        )
    

    def get_by_name(self, name) -> Category | None:
        model = self.session.query(CategoryModel).filter(CategoryModel.name == name).first()
        if not model:
            return None
        return Category (
            id=model.id,
            name=model.name,
            user_id=model.user_id,
            type= model.type,
        )
    
    
    def get_all_by_user_id(self, user_id) -> list[Category]:
        models = (self.session.query(CategoryModel).filter(CategoryModel.user_id == user_id).all())
        return [
            Category(
                id=model.id,
                name=model.name,
                user_id=model.user_id,
                type=model.type,
            )
            for model in models
        ]
    

    def add(self, category: Category) -> Category | None:
        model = CategoryModel(
            id=category.id,
            name=category.name,
            user_id=category.user_id,
            type=category.type,
        )
        self.session.add(model)
