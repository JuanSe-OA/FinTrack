from datetime import datetime, timezone
from uuid import uuid4

import pytest
from app.domain.entities.user import User

def test_user_raises_if_email_is_empty():
    with pytest.raises(ValueError, match="Email cannot be empty"):
        user = User(
            id=uuid4(),
            email="email123@email.com",
            hashed_password= "123456",
            is_active= True,
            created_at=datetime.now(timezone.utc),
        )
    

def test_user_raises_if_email_is_format_invalid():
    with pytest.raises(ValueError, match="Email cannot check the format valid"):
        user = User(
            id=uuid4(),
            email="email123@email.com",
            hashed_password= "123456",
            is_active= True,
            created_at=datetime.now(timezone.utc),
        )


def test_user_created_successfully():
        user = User(
            id=uuid4(),
            email="email123@email.com",
            hashed_password= "123456",
            is_active= True,
            created_at=datetime.now(timezone.utc),
        )


        assert user.email == "email123@email.com"
        assert user.is_active == True
        assert user.hashed_password == "123456"