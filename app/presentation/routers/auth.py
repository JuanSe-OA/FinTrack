from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from app.application.use_cases.user.register_user_use_case import RegisterUserUseCase, RegisterUserCommand
from app.application.use_cases.user.authenticate_user_use_case import AuthenticateUserCommand, AuthenticateUserUseCase
from app.infrastructure.repositories.dynamo_unit_of_work import DynamoUnitOfWork
from app.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from app.infrastructure.security.jwt_token_service import JWTTokenService
from app.infrastructure.config import SECRET_KEY
from fastapi import HTTPException

router = APIRouter(prefix="/auth", tags=["auth"])

password_hasher = BcryptPasswordHasher()
token_service = JWTTokenService(secret_key=SECRET_KEY)

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
    use_case = RegisterUserUseCase(uow, password_hasher)
    try:
        user_id = use_case.execute(RegisterUserCommand(
            email=body.email,
            password=body.password
        ))
        return RegisterRespone(id=str(user_id))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends()):
    uow = DynamoUnitOfWork()
    use_case = AuthenticateUserUseCase(uow, password_hasher, token_service)
    try:
        token = use_case.execute(AuthenticateUserCommand(
            email=form.username,
            password=form.password
        ))
        return TokenResponse(access_token=token, token_type="bearer")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))       