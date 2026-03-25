# tests/unit/application/test_create_budget.py
from decimal import Decimal
from datetime import datetime, timezone
from uuid import uuid4
import pytest
from unittest.mock import MagicMock

from app.application.use_cases.budget.create_budget_use_case import CreateBudgetUseCase, CreateBudgetCommand
from app.domain.entities.user import User
from app.domain.entities.category import Category, CategoryType
from app.domain.entities.budget import Budget


def make_uow():
    uow = MagicMock()
    uow.__enter__ = MagicMock(return_value=uow)
    uow.__exit__ = MagicMock(return_value=False)
    return uow


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


def test_create_budget_raises_if_user_not_found():
    uow = make_uow()
    uow.users.get_by_id.return_value = None

    use_case = CreateBudgetUseCase(uow)
    with pytest.raises(ValueError, match="User not found"):
        use_case.execute(CreateBudgetCommand(
            user_id=uuid4(),
            category_id=uuid4(),
            month=3,
            year=2026,
            limit_amount=Decimal("500")
        ))


def test_create_budget_raises_if_user_inactive():
    uow = make_uow()
    user = make_active_user()
    user.is_active = False
    uow.users.get_by_id.return_value = user

    use_case = CreateBudgetUseCase(uow)
    with pytest.raises(PermissionError, match="User is not active"):
        use_case.execute(CreateBudgetCommand(
            user_id=user.id,
            category_id=uuid4(),
            month=3,
            year=2026,
            limit_amount=Decimal("500")
        ))


def test_create_budget_raises_if_already_exists():
    uow = make_uow()
    user = make_active_user()
    category = make_category(user.id)
    uow.users.get_by_id.return_value = user
    uow.categories.get_by_id.return_value = category
    uow.budgets.get_by_user_category_month_year.return_value = Budget(
        id=uuid4(),
        user_id=user.id,
        category_id=category.id,
        month=3,
        year=2026,
        limit_amount=Decimal("500")
    )

    use_case = CreateBudgetUseCase(uow)
    with pytest.raises(ValueError, match="Budget already exists"):
        use_case.execute(CreateBudgetCommand(
            user_id=user.id,
            category_id=category.id,
            month=3,
            year=2026,
            limit_amount=Decimal("500")
        ))


def test_create_budget_successfully():
    uow = make_uow()
    user = make_active_user()
    category = make_category(user.id)
    uow.users.get_by_id.return_value = user
    uow.categories.get_by_id.return_value = category
    uow.budgets.get_by_user_category_month_year.return_value = None

    use_case = CreateBudgetUseCase(uow)
    result = use_case.execute(CreateBudgetCommand(
        user_id=user.id,
        category_id=category.id,
        month=3,
        year=2026,
        limit_amount=Decimal("500")
    ))

    assert result is not None
    uow.budgets.add.assert_called_once()
    uow.commit.assert_called_once()