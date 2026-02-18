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
            amount=budget.amount,
            year=budget.year,
            month=budget.month,
        )
        self.session.add(model)


        
    def get_by_user_category_month(self, user_id, category_id, year, month) -> Budget | None:
        model = self.session.query(BudgetModel).filter_by(
            user_id=user_id,
            category_id=category_id,
            year=year,
            month=month
        ).first()
        if not model:
            return None
        return Budget(
            id=model.id,
            user_id=model.user_id,
            category_id=model.category_id,
            amount=model.amount,
            year=model.year,
            month=model.month,
        )
    
