from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.transaction import Transaction
from app.domain.entities.user import User
from app.domain.repositories.transaction_repository import TransactionRepository
from app.infrastructure.database.models.transaction_model import TransactionModel
from sqlalchemy import func, extract


class SqlAlchemyTransactionRepository(TransactionRepository):

    def __init__(self, session: Session):
        self.session = session


    def get_by_id(self, transaction_id: UUID) -> Transaction | None:
        model = self.session.get(TransactionModel, transaction_id)
        if not model:
            return None
        return Transaction(
            id=model.id,
            user_id=model.user_id,
            category_id=model.category_id,
            amount=model.amount,
            created_at=model.created_at,
            description=model.description,
        )
    

    def get_total_expenses_for_month(self, user_id, category_id, year, month) -> float:
        total = self.session.query(func.sum(TransactionModel.amount)).filter(
            TransactionModel.user_id == user_id,
            TransactionModel.category_id == category_id,
            extract('year', TransactionModel.created_at) == year,
            extract('month', TransactionModel.created_at) == month
        ).scalar()
        return total or 0.0  
      

    def list_by_user_id(self, user_id) -> list[User]:
        models = self.session.query(TransactionModel).filter(TransactionModel.user_id == user_id).all()
        return [
            Transaction(
                id=model.id,
                user_id=model.user_id,
                category_id=model.category_id,
                amount=model.amount,
                created_at=model.created_at,
                description=model.description,
            )
            for model in models
        ]
    

    def add(self, transaction: Transaction) -> None:
        model = TransactionModel(
            id=transaction.id,
            user_id=transaction.user_id,
            category_id=transaction.category_id,
            amount=transaction.amount,
            created_at=transaction.created_at,
            description=transaction.description,
        )
        self.session.add(model)
