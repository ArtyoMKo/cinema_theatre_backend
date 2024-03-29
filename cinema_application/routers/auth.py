import os
from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from jose import jwt, JWTError
from cinema_application.models import Admins
from cinema_application.database import get_db
from cinema_application.exceptions import AuthenticationFailed

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    # role: str


class Token(BaseModel):
    access_token: str
    token_type: str


DbDependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, database):
    user = database.query(Admins).filter(Admins.username == username).first()
    if user and bcrypt_context.verify(password, user.hashed_password):
        return user
    return False


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    secret_key = os.environ["JWT_SECRET_KEY"]
    algorithm = os.environ["JWT_ALGORITHM"]

    encode = {
        "sub": username,
        "id": user_id,
        "role": role,
        "exp": datetime.utcnow() + expires_delta,
    }
    return jwt.encode(encode, secret_key, algorithm)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    secret_key = os.environ["JWT_SECRET_KEY"]
    algorithm = os.environ["JWT_ALGORITHM"]
    try:
        payload = jwt.decode(token, secret_key, algorithm)
        username: str = payload.get("sub")  # type: ignore
        user_id: int = payload.get("id")  # type: ignore
        user_role: str = payload.get("role")  # type: ignore
        if username is None or user_id is None:
            raise AuthenticationFailed
        return {"username": username, "id": user_id, "user_role": user_role}
    except JWTError:
        raise AuthenticationFailed  # pylint: disable=raise-missing-from


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(database: DbDependency, create_user_request: CreateUserRequest):
    """
    Create new superuser (admin) account.
    Superuser account needs for managing theatre rooms, movies, movie sessions.
    """
    create_user_model = Admins(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        # role=create_user_request.role,
    )

    database.add(create_user_model)
    database.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], database: DbDependency
):
    user = authenticate_user(form_data.username, form_data.password, database)
    if not user:
        raise AuthenticationFailed
    token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=30)
    )
    return {"access_token": token, "token_type": "bearer"}
