from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

import pytest
from app.domain.entities.transaction import Transaction

def test_transaction_raises_if_amount_is_zero():
    with pytest.raises(ValueError, match="Amount must be positive"):
        Transaction(
            id=uuid4(),
            user_id=uuid4(),
            category_id=uuid4(),
            amount=Decimal("0"),
            created_at=datetime.now(timezone.utc),
        )
    

def test_transaction_raises_if_amount_is_negative():
    with pytest.raises(ValueError, match="Amount must be positive"):
        Transaction(
            id=uuid4(),
            user_id=uuid4(),
            category_id=uuid4(),
            amount=Decimal("-10"),
            created_at=datetime.now(timezone.utc),
        )
def test_transaction_created_successfully():
    transaction = Transaction(
            id=uuid4(),
            user_id=uuid4(),
            category_id=uuid4(),
            amount=Decimal("5500"),
            created_at=datetime.now(timezone.utc),
        )
    assert transaction.amount == Decimal("5500")
    assert transaction.description is None