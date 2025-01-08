from pydantic import BaseModel
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
