from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4
from datetime import datetime, timezone
from app.domain.entities.alert import Alert
from app.application.unit_of_work import UnitOfWork
from app.domain.entities.transaction import Transaction
from app.domain.services.notification_service import NotificationService



@dataclass
class CreateTransactionCommand:
    user_id: UUID
    category_id: UUID
    amount: Decimal
    description: str | None = None


class CreateTransactionUseCase:

    def __init__(self, uow: UnitOfWork, notification_service: NotificationService):
        self.uow = uow
        self.notification_service = notification_service

    def execute(self, cmd: CreateTransactionCommand) -> UUID:
        with self.uow:
            # 1. Validar que el usuario existe y está activo
            user = self.uow.users.get_by_id(cmd.user_id)
            if user is None:
                raise ValueError("User not found")
            if not user.is_active:
                raise PermissionError("User is not active")

            # 2. Validar que la categoría pertenece al usuario
            category = self.uow.categories.get_by_id(cmd.category_id)
            if category is None or category.user_id != cmd.user_id:
                raise ValueError("Category not found")

            # 3. Crear la entidad — la validación de amount > 0 ocurre aquí
            transaction = Transaction(
                id=uuid4(),
                user_id=cmd.user_id,
                category_id=cmd.category_id,
                amount=cmd.amount,
                created_at=datetime.now(timezone.utc),
                description=cmd.description,
            )

            # 4. Persistir
            self.uow.transactions.add(transaction)

            # 5. Verificar presupuesto y generar alerta si corresponde
            now = transaction.created_at
            total = self.uow.transactions.get_total_expenses_for_month(
                cmd.user_id, cmd.category_id, now.year, now.month
            )
            budget = self.uow.budgets.get_by_user_category_month(
                cmd.user_id, cmd.category_id, now.year, now.month
            )
            if budget and total > float(budget.limit_amount):
                alert = Alert(
                    id=uuid4(),
                    user_id=cmd.user_id,
                    message=f"Budget exceeded for category {cmd.category_id}",
                    read=False,
                    created_at=datetime.now(timezone.utc),
                )
                self.uow.alerts.add(alert)
                self.notification_service.send_budget_exceeded(
                    user_email=user.email,
                    category_name=category.name,
                    spent=total,
                    limit=float(budget.limit_amount),
                )

            self.uow.commit()
            return transaction.id