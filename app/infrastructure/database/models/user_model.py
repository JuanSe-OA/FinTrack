from datetime import datetime
from sqlalchemy import (
    String, Boolean, DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database.base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relaciones
    categories = relationship("CategoryModel", back_populates="user", cascade="all, delete")
    transactions = relationship("TransactionModel", back_populates="user", cascade="all, delete")
    budgets = relationship("BudgetModel", back_populates="user", cascade="all, delete")
    alerts = relationship("AlertModel", back_populates="user", cascade="all, delete")

