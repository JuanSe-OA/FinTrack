from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.application.unit_of_work import UnitOfWork
from app.domain.entities.user import User
from app.domain.services.password_hasher import PasswordHasher


@dataclass
class RegisterUserCommand:
    email: str
    password: str

class RegisterUserUseCase:
    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher):
        self.uow = uow
        self.password_hasher = password_hasher

    def execute(self, command: RegisterUserCommand) -> UUID:
        with self.uow:
            existing_user = self.uow.user_repo.find_by_email(command.email)
            if existing_user:
                raise ValueError("Email already registered")

            hashed_password = self.password_hasher.hash(command.password)
            user = User (
                id= uuid4(),
                email=command.email,
                hashed_password=hashed_password,
                is_active=True,
                created_at=datetime.now(timezone.utc),
            )
            self.uow.transactions.add(user)
            self.uow.commit()
            return user.id