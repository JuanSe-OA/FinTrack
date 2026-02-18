from datetime import datetime
from decimal import Decimal
from sqlalchemy import (
    String, Boolean, DateTime, ForeignKey,
    Numeric, Text, Integer, CheckConstraint,
    UniqueConstraint, Index
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.infrastructure.database.base import Base

class BudgetModel(Base):
    __tablename__ = "budgets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False
    )

    month: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    __table_args__ = (
        CheckConstraint("limit_amount > 0", name="chk_budget_positive"),
        CheckConstraint("month BETWEEN 1 AND 12", name="chk_month_valid"),
        UniqueConstraint("user_id", "category_id", "month", "year", name="uq_budget_unique"),
    )

    user = relationship("UserModel", back_populates="budgets")