from dataclasses import dataclass
from uuid import UUID

from app.application.unit_of_work import UnitOfWork

@dataclass
class GetBudgetStatusCommand:
    user_id: UUID
    category_id: UUID
    month: int
    year: int

class GetBudgetStatusUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def execute(self, cmd: GetBudgetStatusCommand) -> dict:
        with self.uow:
            user = self.uow.users.get_by_id(cmd.user_id)
            if user is None:
                raise ValueError("User not found")

            if not user.is_active:
                raise PermissionError("User is not active")

            budget = self.uow.budgets.get_by_user_category_month_year(cmd.user_id,cmd.category_id, cmd.month, cmd.year)
            if budget is None:
                raise ValueError("Budget not found")
            total_expense = self.uow.transactions.get_total_expenses_for_month(cmd.user_id,cmd.category_id,cmd.year,cmd.month)
            category = self.uow.categories.get_by_id(cmd.category_id)                                                                 ,
                                                                                
            return {
                "category_name": category.name,
                "budgeted_amount": budget.limit_amount,
                "total_expense": total_expense,
                "remaining_budget": float(budget.limit_amount) - total_expense,
                "exceeded" : total_expense > float(budget.limit_amount)
                }

            