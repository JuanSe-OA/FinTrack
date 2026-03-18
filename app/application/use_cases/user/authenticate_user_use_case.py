from dataclasses import dataclass

from app.application.unit_of_work import UnitOfWork
from app.domain.services.notification_service import NotificationService
from app.domain.services.password_hasher import PasswordHasher
from app.domain.services.token_service import TokenService


@dataclass
class AuthenticateUserCommand:
    email: str
    password: str

class AuthenticateUserUseCase:
    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher, token_service: TokenService, notification:NotificationService) :
        self.uow = uow
        self.password_hasher = password_hasher
        self.token_service = token_service
        self.notification = notification

    def execute(self, cmd: AuthenticateUserCommand) -> str:
        with self.uow:
            user = self.uow.users.get_by_email(cmd.email)
            if user is None:
                raise ValueError("Invalid credentials")
            if not self.password_hasher.verify(cmd.password, user.hashed_password):
                raise ValueError("Invalid credentials")
            if not user.is_active:
                raise PermissionError("User is not active")

            self.notification.send_login_notification(user.email)
            return self.token_service.generate(user.id)

