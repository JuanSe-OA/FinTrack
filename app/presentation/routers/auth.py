from fastapi import APIRouter, Depends, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from app.application.use_cases.user.register_user_use_case import RegisterUserUseCase, RegisterUserCommand
from app.application.use_cases.user.authenticate_user_use_case import AuthenticateUserCommand, AuthenticateUserUseCase
from app.infrastructure.notifications.sqs_notification_service import SqsNotificationService
from app.infrastructure.repositories.dynamo_unit_of_work import DynamoUnitOfWork
from app.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from app.infrastructure.security.jwt_token_service import JWTTokenService
from app.infrastructure.config import SECRET_KEY
from fastapi import HTTPException

router = APIRouter(prefix="/auth", tags=["auth"])

password_hasher = BcryptPasswordHasher()
token_service = JWTTokenService(secret_key=SECRET_KEY)
notification_service = SqsNotificationService()

#Schemas

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRespone(BaseModel):
    id : str

class TokenResponse(BaseModel):
    access_token : str
    token_type : str



#Endpoints

@router.post("/register", response_model=RegisterRespone, status_code=201)
def register(body: RegisterRequest):
    uow = DynamoUnitOfWork()
    use_case = RegisterUserUseCase(uow, password_hasher, notification_service)
    try:
        user_id = use_case.execute(RegisterUserCommand(
            email=body.email,
            password=body.password
        ))
        return RegisterRespone(id=str(user_id))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login", response_model=TokenResponse)
def login(
    username: str = Form(..., description="User email"),
    password: str = Form(..., description="Password User")
):
    uow = DynamoUnitOfWork()
    use_case = AuthenticateUserUseCase(uow, password_hasher, token_service, notification_service)
    
    try:
        token = use_case.execute(AuthenticateUserCommand(
            email=username,
            password=password
        ))
        return TokenResponse(access_token=token, token_type="bearer")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 


@router.post("/login/debug")
async def login_debug(request: Request):
    body = await request.body()
    form = await request.form()
    return {"body": body.decode(), "form": dict(form), "headers": dict(request.headers)}      