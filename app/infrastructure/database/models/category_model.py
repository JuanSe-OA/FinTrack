from datetime import datetime
from sqlalchemy import (
    String, Boolean, DateTime, ForeignKey,
    Numeric, Text, Integer, CheckConstraint,
    UniqueConstraint, Index
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.infrastructure.database.base import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_category_name"),
        CheckConstraint("type IN ('INCOME', 'EXPENSE')", name="chk_category_type"),
    )

    user = relationship("UserModel", back_populates="categories")
    transactions = relationship("TransactionModel", back_populates="category", cascade="all, delete")

