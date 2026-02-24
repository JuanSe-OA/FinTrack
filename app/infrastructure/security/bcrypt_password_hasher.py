import bcrypt
from app.domain.services.password_hasher import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):

    def hash(self, plain_password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_password.encode(), salt).decode()

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())