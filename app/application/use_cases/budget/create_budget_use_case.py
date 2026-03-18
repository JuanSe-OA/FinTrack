from dataclasses import dataclass
from decimal import Decimal

from app.application.unit_of_work import UnitOfWork
from uuid import UUID, uuid4
from datetime import date, datetime

from app.domain.entities.budget import Budget


@dataclass
class CreateBudgetCommand:
    user_id: UUID
    category_id: UUID
    month: int
    year: int
    limit_amount: Decimal


class CreateBudgetUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def execute(self, cmd: CreateBudgetCommand) -> UUID:
        with self.uow:
            user = self.uow.users.get_by_id(cmd.user_id)
            if user is None:
                raise ValueError("User not found")

            if not user.is_active:
                raise PermissionError("User is not active")

            category = self.uow.categories.get_by_id(cmd.user_id,cmd.category_id)
            if category is None or category.user_id != cmd.user_id:
                raise ValueError("Category not found")

            existing = self.uow.budgets.get_by_user_category_month_year(
                cmd.user_id, cmd.category_id, cmd.month, cmd.year
            )
            if existing:
                raise ValueError("Budget already exists for this month")

            budget = Budget(
                id=uuid4(),
                user_id=cmd.user_id,
                category_id=cmd.category_id,
                month=cmd.month,
                year=cmd.year,
                limit_amount=cmd.limit_amount,
            )
            self.uow.budgets.add(budget)
            self.uow.commit()
            return budget.id
