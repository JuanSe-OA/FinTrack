from datetime import datetime
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.use_cases.transaction.create_transaction_use_case import CreateTransactionCommand, CreateTransactionUseCase
from app.application.use_cases.transaction.get_monthly_expense_summary_use_case import GetMonthlyExpenseSummaryCommand, GetMonthlyExpenseSummaryUseCase
from app.application.use_cases.transaction.list_user_transaction_use_case import ListUserTransactionUseCase
from app.domain.services import notification_service
from app.infrastructure.sql_alchemy_unit_of_work import SqlAlchemyUnitOfWork
from app.presentation.dependencies import get_current_user_id


router = APIRouter(prefix="/transactions", tags=["Transactions"])

#Schemas
class CreateTransactionRequest(BaseModel):
    category_id : UUID
    amount : Decimal
    created_at : datetime
    description : str | None = None


class TransactionResponse(BaseModel):
    id: str
    category_id: str
    amount: Decimal
    description: str | None

#Endpoints

@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(
    body: CreateTransactionRequest,
    user_id: UUID = Depends(get_current_user_id)
):
    uow = SqlAlchemyUnitOfWork()
    use_case = CreateTransactionUseCase(uow, notification_service)
    try:
        transaction_id = use_case.execute(CreateTransactionCommand(
            user_id=user_id,
            category_id=body.category_id,
            amount=body.amount,
            description=body.description,
        ))
        return TransactionResponse(
            id=str(transaction_id),
            category_id=str(body.category_id),
            amount=body.amount,
            description=body.description,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/", response_model=list[TransactionResponse])
def list_user_transactions(user_id: UUID = Depends(get_current_user_id)):
    uow = SqlAlchemyUnitOfWork()
    use_case = ListUserTransactionUseCase(uow)
    transactions = use_case.execute(user_id)
    return [{"id": str(c.id), "category_id": c.category_id, "amount": float(c.amount), "description" : c.description} for c in transactions]


@router.get("/summary", response_model=dict[str, float])
def get_monthly_expense_summary(
    month: int,
    year: int,
    user_id: UUID = Depends(get_current_user_id)
):
    uow = SqlAlchemyUnitOfWork()
    use_case = GetMonthlyExpenseSummaryUseCase(uow)
    try:
        summary = use_case.execute(GetMonthlyExpenseSummaryCommand(
            user_id=user_id,
            month=month,
            year=year
        ))
        return summary
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
