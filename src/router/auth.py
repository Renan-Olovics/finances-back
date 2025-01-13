from fastapi import APIRouter, Query, HTTPException
from bcrypt import hashpw, gensalt, checkpw
from http import HTTPStatus
from jwt import encode

from src.models import UserData, UserResponse, LoginData
from src.database import session
from src.database import User

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/register", status_code=HTTPStatus.CREATED, response_model=UserResponse)
def register_user(data: UserData):
    hashed_password = hashpw(data.password.encode("utf8"), gensalt())
    data.password = hashed_password
    data.email = data.email.lower()
    if session.query(User).filter(User.email == data.email).first():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Unable to register. Please check your information.",
        )

    user = User(name=data.name, email=data.email, password=data.password.decode("utf8"))

    session.add(user)
    session.commit()

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        token=encode(
            {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
            },
            "secret",
            algorithm="HS256",
        ),
    )


@router.post("/login", status_code=HTTPStatus.OK, response_model=UserResponse)
def login_user(data: LoginData):
    data.email = data.email.lower()
    user = session.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not checkpw(data.password.encode(), user.password.encode()):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        token=encode(
            {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
            },
            "secret",
            algorithm="HS256",
        ),
    )
