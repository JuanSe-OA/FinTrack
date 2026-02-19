from datetime import datetime

from app.domain.entities.budget import Budget
from sqlalchemy.orm import Session
from app.domain.repositories.budget_repository import BudgetRepository
from app.infrastructure.database.models.budget_model import BudgetModel


class SqlAlchemyBudgetRepository(BudgetRepository):
    def __init__(self, session: Session):
        self.session = session


    def add(self, budget: Budget) -> None:
        model = BudgetModel(
            id=budget.id,
            user_id=budget.user_id,
            category_id=budget.category_id,
            month=budget.month,
            year=budget.year,
            limit_amount=budget.limit_amount,
            
        )
        self.session.add(model)


        
    def get_by_user_category_month(self, user_id, category_id, month, year) -> Budget | None:
        model = self.session.query(BudgetModel).filter_by(
            user_id=user_id,
            category_id=category_id,
            month=month,
            year= year
        ).first()
        if not model:
            return None
        return Budget(
            id=model.id,
            user_id=model.user_id,
            category_id=model.category_id,
            month=model.month,
            year=model.year,
            limit_amount=model.limit_amount
            
        )
    
