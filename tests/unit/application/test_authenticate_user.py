# Helpers
from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.application.use_cases.user.authenticate_user_use_case import AuthenticateUserCommand, AuthenticateUserUseCase
from app.domain.entities.user import User


def make_active_user():
    return User(
        id=uuid4(),
        email="test@test.com",
        hashed_password="123456",
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )


def make_uow():
    uow = MagicMock()
    uow.__enter__ = MagicMock(return_value=uow)
    uow.__exit__ = MagicMock(return_value=False)
    return uow


def test_authenticate_raises_if_user_not_found():
    uow = make_uow()
    uow.users.get_by_email.return_value = None  
    password_hasher = MagicMock()
    token_service = MagicMock()
    notification_service = MagicMock()

    use_case = AuthenticateUserUseCase(uow, password_hasher, token_service, notification_service)

    with pytest.raises(ValueError, match="Invalid credentials"): 
        use_case.execute(AuthenticateUserCommand(
            email="test@test.com",
            password="123456"
        ))


def test_authenticate_raises_if_wrong_password():
    uow = make_uow()
    user = make_active_user()
    uow.users.get_by_email.return_value = user  
    password_hasher = MagicMock()
    password_hasher.verify.return_value = False
    token_service = MagicMock()
    notification_service = MagicMock()

    use_case = AuthenticateUserUseCase(uow, password_hasher, token_service, notification_service)

    with pytest.raises(ValueError, match="Invalid credentials"): 
        use_case.execute(AuthenticateUserCommand(
            email="test@test.com",
            password="wrong_password"
        ))


def test_authenticate_raises_if_user_inactive():
    uow = make_uow()
    user = make_active_user()
    user.is_active = False
    uow.users.get_by_email.return_value = user  
    password_hasher = MagicMock()
    password_hasher.verify.return_value = True
    token_service = MagicMock()
    notification_service = MagicMock()

    use_case = AuthenticateUserUseCase(uow, password_hasher, token_service, notification_service)

    with pytest.raises(PermissionError, match="User is not active"): 
        use_case.execute(AuthenticateUserCommand(
            email="test@test.com",
            password="123456"
        ))
        

def test_authenticate_sends_login_notification():
    uow = make_uow()
    user = make_active_user()
    uow.users.get_by_email.return_value = user  
    password_hasher = MagicMock()
    password_hasher.verify.return_value = True
    token_service = MagicMock()
    notification_service = MagicMock()

    use_case = AuthenticateUserUseCase(uow, password_hasher, token_service, notification_service)

    use_case.execute(AuthenticateUserCommand(
            email="test@test.com",
            password="123456"
        ))
    notification_service.send_login_notification.assert_called_once_with(user.email)



def test_authenticate_returns_token():
    uow = make_uow()
    user = make_active_user()
    uow.users.get_by_email.return_value = user

    password_hasher = MagicMock()
    password_hasher.verify.return_value = True 

    token_service = MagicMock()
    token_service.generate.return_value = "fake_token"  

    notification_service = MagicMock()

    use_case = AuthenticateUserUseCase(uow, password_hasher, token_service, notification_service)
    result = use_case.execute(AuthenticateUserCommand(
        email="test@test.com",
        password="123456"
    ))

    assert result == "fake_token"


