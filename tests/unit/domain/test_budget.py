from decimal import Decimal
from uuid import uuid4
import pytest

from app.domain.entities.budget import Budget


def test_budget_raises_if_limit_amount_is_zero():
    with pytest.raises(ValueError, match="Budget must be positive"):
        Budget(
            id=uuid4(),
            user_id=uuid4(),
            category_id=uuid4(),
            month=3,
            year=2026,
            limit_amount=Decimal("0")
        )

def test_budget_raises_if_limit_amount_is_negative():
    with pytest.raises(ValueError, match="Budget must be positive"):
        Budget(
            id=uuid4(),
            user_id=uuid4(),
            category_id=uuid4(),
            month=3,
            year=2026,
            limit_amount=Decimal("-100")
        )

def test_budget_raises_if_year_is_in_the_past():
    with pytest.raises(ValueError, match="Budget can't be in the past"):
        Budget(
            id=uuid4(),
            user_id=uuid4(),
            category_id=uuid4(),
            month=3,
            year=2020,
            limit_amount=Decimal("500")
        )

def test_budget_created_successfully():
    budget = Budget(
        id=uuid4(),
        user_id=uuid4(),
        category_id=uuid4(),
        month=3,
        year=2026,
        limit_amount=Decimal("500")
    )
    assert budget.limit_amount == Decimal("500")
    assert budget.year == 2026