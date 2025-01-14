from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from bcrypt import hashpw, gensalt, checkpw
from http import HTTPStatus
from jwt import encode

from src.models import UserData, UserResponse, LoginData, Token
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

    if not verify_password(data.password, user.password):
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


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    print("❓❓❓", form_data)
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Incorrect email or password",
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Incorrect email or password",
        )

    access_token = encode(
        {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
        },
        "secret",
        algorithm="HS256",
    )

    return {"access_token": access_token, "token_type": "bearer"}


def verify_password(plain_password, hashed_password):
    return checkpw(plain_password.encode(), hashed_password.encode())
