from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

import pytest
from unittest.mock import MagicMock

from app.application.use_cases.transaction.create_transaction_use_case import CreateTransactionUseCase, CreateTransactionCommand
from app.domain.entities.user import User
from app.domain.entities.category import Category, CategoryType
from app.domain.entities.budget import Budget


# Helpers
def make_active_user():
    return User(
        id=uuid4(),
        email="test@test.com",
        hashed_password="hashed",
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )


def make_category(user_id):
    return Category(
        id=uuid4(),
        user_id=user_id,
        name="Comida",
        type=CategoryType.EXPENSE
    )


def make_budget(user_id, category_id):
    return Budget(
        id=uuid4(),
        user_id=user_id,
        category_id=category_id,
        month=datetime.now().month,
        year=datetime.now().year,
        limit_amount=Decimal("100")
    )


def make_uow():
    uow = MagicMock()
    uow.__enter__ = MagicMock(return_value=uow)
    uow.__exit__ = MagicMock(return_value=False)
    return uow


# Tests
def test_create_transaction_raises_if_user_not_found():
    uow = make_uow()
    uow.users.get_by_id.return_value = None

    use_case = CreateTransactionUseCase(uow, MagicMock())
    with pytest.raises(ValueError, match="User not found"):
        use_case.execute(CreateTransactionCommand(
            user_id=uuid4(),
            category_id=uuid4(),
            amount=Decimal("100"),
        ))


def test_create_transaction_raises_if_user_inactive():
    uow = make_uow()
    inactive_user = make_active_user()
    inactive_user.is_active = False
    uow.users.get_by_id.return_value = inactive_user

    use_case = CreateTransactionUseCase(uow, MagicMock())
    with pytest.raises(PermissionError, match="User is not active"):
        use_case.execute(CreateTransactionCommand(
            user_id=uuid4(),
            category_id=uuid4(),
            amount=Decimal("100"),
        ))


def test_create_transaction_raises_if_category_not_found():
    uow = make_uow()
    user = make_active_user()
    uow.users.get_by_id.return_value = user
    uow.categories.get_by_id.return_value = None

    use_case = CreateTransactionUseCase(uow, MagicMock())
    with pytest.raises(ValueError, match="Category not found"):
        use_case.execute(CreateTransactionCommand(
            user_id=user.id,
            category_id=uuid4(),
            amount=Decimal("100"),
        ))


def test_create_transaction_creates_alert_when_budget_exceeded():
    uow = make_uow()
    user = make_active_user()
    category = make_category(user.id)
    budget = make_budget(user.id, category.id)

    uow.users.get_by_id.return_value = user
    uow.categories.get_by_id.return_value = category
    uow.budgets.get_by_user_category_month.return_value = budget
    uow.transactions.get_total_expenses_for_month.return_value = 150.0 

    notification_service = MagicMock()
    use_case = CreateTransactionUseCase(uow, notification_service)
    use_case.execute(CreateTransactionCommand(
        user_id=user.id,
        category_id=category.id,
        amount=Decimal("50"),
    ))

    uow.alerts.add.assert_called_once()
    notification_service.send_budget_exceeded.assert_called_once()

