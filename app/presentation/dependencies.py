from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID

from app.infrastructure.security.jwt_token_service import JWTTokenService
from app.infrastructure.config import SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
token_service = JWTTokenService(secret_key=SECRET_KEY)


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> UUID:
    try:
        return token_service.decode(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )