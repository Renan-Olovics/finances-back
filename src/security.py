from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from http import HTTPStatus
from jwt import decode, DecodeError
from sqlalchemy import select
from src.database import session

from src.database import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token, "secret", algorithms=["HS256"])
        user_id = payload.get("id")

        if user_id is None:
            raise credentials_exception

    except DecodeError:

        raise credentials_exception

    user = session.execute(select(User).filter(User.id == user_id)).first()

    if not user:
        raise credentials_exception

    return user
