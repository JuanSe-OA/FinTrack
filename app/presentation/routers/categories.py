from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.application.use_cases.category.create_category_use_case import CreateCategoryUseCase, CreateCategoryCommand
from app.application.use_cases.category.delete_category_use_case import DeleteCategoryUseCase
from app.application.use_cases.category.list_user_categories_use_case import ListUserCategoriesUseCase
from app.domain.entities.category import CategoryType
from app.infrastructure.repositories.dynamo_unit_of_work import DynamoUnitOfWork
from app.presentation.dependencies import get_current_user_id
from fastapi import HTTPException


router = APIRouter(prefix="/categories", tags=["Categories"])

#Schemas
class CreateCategoryRequest(BaseModel):
    name : str
    type : CategoryType
    description: str | None = None


class CategoryResponse(BaseModel):
    id: str
    name: str
    type: str

#Endpoints

@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    body: CreateCategoryRequest,
    user_id: UUID = Depends(get_current_user_id)  
):
    uow = DynamoUnitOfWork()
    use_case = CreateCategoryUseCase(uow)
    try:
        category_id = use_case.execute(CreateCategoryCommand(
            user_id=user_id,
            name=body.name,
            type=body.type,
            description= body.description
        ))
        return CategoryResponse(id=str(category_id), name=body.name, type=body.type.value)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get("/", response_model=list[CategoryResponse])
def list_categories(user_id: UUID = Depends(get_current_user_id)):
    uow = DynamoUnitOfWork()
    use_case = ListUserCategoriesUseCase(uow)
    categories = use_case.execute(user_id)
    return [{"id": str(c.id), "name": c.name, "type": c.type.value} for c in categories]


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: UUID,
    user_id: UUID = Depends(get_current_user_id)
):
    uow = DynamoUnitOfWork()
    use_case = DeleteCategoryUseCase(uow)
    try:
        use_case.execute(category_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
