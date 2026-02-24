from dataclasses import dataclass
from uuid import UUID

from app.application.unit_of_work import UnitOfWork
from app.domain.entities.category import CategoryType


@dataclass
class GetMonthlyExpenseSummaryCommand:
    user_id: UUID
    month: int
    year: int


class GetMonthlyExpenseSummaryUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def execute(self, cmd: GetMonthlyExpenseSummaryCommand) -> dict[str,float]:
        with self.uow:
            user = self.uow.users.get_by_id(cmd.user_id)
            if user is None:
                raise ValueError("User not found")

            if not user.is_active:
                raise PermissionError("User is not active")
            
            categories = self.uow.categories.get_all_by_user_id_and_type(cmd.user_id, CategoryType.EXPENSE)
            summary = {}
            for category in categories:
                total = self.uow.transactions.get_total_expenses_for_month(
                    cmd.user_id, category.id, cmd.month, cmd.year
                )
                if total > 0:
                    summary[str(category.name)] = total

            return summary
