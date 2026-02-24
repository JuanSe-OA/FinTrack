from fastapi import FastAPI

from app.infrastructure.config import (
    SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SMTP_SENDER, SECRET_KEY
)
from app.infrastructure.notifications.smtp_notification_service import SmtpNotificationService
from app.infrastructure.security.jwt_token_service import JWTTokenService
from app.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from app.presentation.routers import alerts, auth, budgets, categories, transactions

app = FastAPI(title="FinTrack API")

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(budgets.router)
app.include_router(alerts.router)

password_hasher = BcryptPasswordHasher()
token_service = JWTTokenService(secret_key=SECRET_KEY)
notification_service = SmtpNotificationService(
    host=SMTP_HOST,
    port=SMTP_PORT,
    username=SMTP_USERNAME,
    password=SMTP_PASSWORD,
    sender=SMTP_SENDER
)