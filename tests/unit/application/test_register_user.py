# tests/unit/application/test_register_user.py
from datetime import datetime, timezone
from uuid import uuid4
import pytest
from unittest.mock import MagicMock

from app.application.use_cases.user.register_user_use_case import RegisterUserUseCase, RegisterUserCommand
from app.domain.entities.user import User


def make_uow():
    uow = MagicMock()
    uow.__enter__ = MagicMock(return_value=uow)
    uow.__exit__ = MagicMock(return_value=False)
    return uow


def test_register_raises_if_email_already_exists():
    uow = make_uow()
    uow.users.get_by_email.return_value = User(
        id=uuid4(),
        email="test@test.com",
        hashed_password="hashed",
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    password_hasher = MagicMock()
    notification_service = MagicMock()

    use_case = RegisterUserUseCase(uow, password_hasher, notification_service)
    with pytest.raises(ValueError, match="Email already registered"):
        use_case.execute(RegisterUserCommand(
            email="test@test.com",
            password="123456"
        ))


def test_register_creates_user_successfully():
    uow = make_uow()
    uow.users.get_by_email.return_value = None
    password_hasher = MagicMock()
    password_hasher.hash.return_value = "hashed_password"
    notification_service = MagicMock()

    use_case = RegisterUserUseCase(uow, password_hasher, notification_service)
    result = use_case.execute(RegisterUserCommand(
        email="test@test.com",
        password="123456"
    ))

    assert result is not None
    uow.users.add.assert_called_once()
    uow.commit.assert_called_once()


def test_register_sends_welcome_notification():
    uow = make_uow()
    uow.users.get_by_email.return_value = None
    password_hasher = MagicMock()
    password_hasher.hash.return_value = "hashed_password"
    notification_service = MagicMock()

    use_case = RegisterUserUseCase(uow, password_hasher, notification_service)
    use_case.execute(RegisterUserCommand(
        email="test@test.com",
        password="123456"
    ))

    notification_service.send_welcome.assert_called_once_with("test@test.com")