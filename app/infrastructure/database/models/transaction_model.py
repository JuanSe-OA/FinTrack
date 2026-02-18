from datetime import datetime
from decimal import Decimal
from sqlalchemy import (
    String, Boolean, DateTime, ForeignKey, Numeric, Text, CheckConstraint, Index
)
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database.base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid

class TransactionModel(Base):
    __tablename__ = "transactions"

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

    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("amount > 0", name="chk_amount_positive"),
        Index("idx_transaction_user_date", "user_id", "created_at"),
    )

    user = relationship("UserModel", back_populates="transactions")
    category = relationship("CategoryModel", back_populates="transactions")
