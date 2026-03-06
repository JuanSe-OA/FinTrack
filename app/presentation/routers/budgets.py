from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.use_cases.budget.create_budget_use_case import CreateBudgetUseCase
from app.application.use_cases.budget.get_budget_status_use_case import GetBudgetStatusCommand, GetBudgetStatusUseCase
from app.application.use_cases.budget.update_budget_use_case import UpdateBudgetCommand, UpdateBudgetUseCase
from app.infrastructure.repositories.dynamo_unit_of_work import DynamoUnitOfWork
from app.presentation.dependencies import get_current_user_id


router = APIRouter(prefix="/budgets", tags=["Budgets"])

# Schemas
class CreateBudgetRequest(BaseModel):
    category_id: UUID
    month: int
    year: int
    limit_amount: Decimal

class CreateBudgetResponse(BaseModel):
    id: str

class BudgetStatusResponse(BaseModel):
    category_name: str
    limit_amount: float
    total_spent: float
    remaining: float
    exceeded: bool

class UpdateBudgetRequest(BaseModel):
    limit_amount: Decimal

class UpdateBudgetResponse(BaseModel):
    id: str
    limit_amount: float


@router.post("/", response_model=CreateBudgetResponse, status_code=201)
def create_budget(
    body: CreateBudgetRequest,
    user_id: UUID = Depends(get_current_user_id)  
):
    uow = DynamoUnitOfWork()
    use_case = CreateBudgetUseCase(uow)
    try:
        budget_id = use_case.execute(CreateBudgetUseCase(
            user_id=user_id,
            category_id=body.category_id,
            month=body.month,
            year=body.year,
            limit_amount=body.limit_amount
        ))
        return CreateBudgetResponse(id=str(budget_id))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get("/status", response_model=BudgetStatusResponse)
def get_budget_status(
    category_id: UUID,
    month: int,
    year: int,
    user_id: UUID = Depends(get_current_user_id)
):
    uow = DynamoUnitOfWork()
    use_case = GetBudgetStatusUseCase(uow)
    try:
        status = use_case.execute(GetBudgetStatusCommand(
            user_id=user_id,
            category_id=category_id,
            month=month,
            year=year
        ))
        return BudgetStatusResponse(**status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.put("/{budget_id}", response_model=UpdateBudgetResponse)
def update_budget(
    budget_id: UUID,
    body: UpdateBudgetRequest,
    user_id: UUID = Depends(get_current_user_id)
):
    uow = DynamoUnitOfWork()
    use_case = UpdateBudgetUseCase(uow)
    try:
        use_case.execute(UpdateBudgetCommand(
            budget_id=budget_id,
            limit_amount=body.limit_amount
        ))
        return UpdateBudgetResponse(id=str(budget_id), limit_amount=float(body.limit_amount))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))