from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from app.application.unit_of_work import UnitOfWork

@dataclass
class UpdateBudgetCommand:
    budget_id: UUID
    limit_amount: Decimal


class UpdateBudgetUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def execute(self, cmd: UpdateBudgetCommand) -> None:   
        with self.uow:
            budget = self.uow.budgets.get_by_id(cmd.budget_id)
            if budget is None:
                raise ValueError(f"Budget not found")
            if cmd.limit_amount < 0:
                raise ValueError("Limit amount must be non-negative")
            budget.limit_amount = cmd.limit_amount
            self.uow.budgets.update(budget)
            self.uow.commit()