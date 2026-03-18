from datetime import datetime, timedelta, timezone
from uuid import UUID
from app.domain.services.token_service import TokenService
import jwt

class JWTTokenService(TokenService):

    def __init__(self, secret_key: str, expiration_minutes: int = 60):
        self.secret_key = secret_key
        self.expiration_minutes = expiration_minutes

    def generate(self, user_id: UUID) -> str:
        print(f"Generating token for user_id: {user_id}")
        print(f"Secret key: {self.secret_key}")
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self.expiration_minutes)
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def decode(self, token: str) -> UUID:
        payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
        return UUID(payload["sub"])