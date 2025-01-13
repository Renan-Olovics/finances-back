from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from enum import Enum


class TransactionTypeEnum(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class TransactionData(BaseModel):
    amount: float
    date: datetime
    type: TransactionTypeEnum


class TransactionResponse(TransactionData):
    id: UUID


class UserData(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    token: str


class LoginData(BaseModel):
    email: EmailStr
    password: str
