from fastapi import APIRouter, Query, HTTPException
from http import HTTPStatus
from uuid import UUID

from src.database import Transaction, session
from src.models import TransactionResponse, TransactionData

router = APIRouter(tags=["Transaction"])


@router.post(
    "/transaction", status_code=HTTPStatus.CREATED, response_model=TransactionResponse
)
def create_transaction(transaction_data: TransactionData):
    transaction = Transaction(
        amount=transaction_data.amount,
        date=transaction_data.date,
        type=transaction_data.type,
    )

    session.add(transaction)
    session.commit()

    return transaction


@router.get(
    "/transaction/{transaction_id}",
    response_model=TransactionResponse,
    status_code=HTTPStatus.OK,
)
def read_transaction(transaction_id: UUID):
    if not transaction:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Transaction not found"
        )

    transaction = session.query(Transaction).get(transaction_id)
    return transaction


@router.get(
    "/transaction",
    response_model=list[TransactionResponse],
    status_code=HTTPStatus.OK,
)
def read_transactions(limit: int = Query(10, le=100), offset: int = Query(0, ge=0)):
    transactions = session.query(Transaction).offset(offset).limit(limit).all()
    return transactions


@router.put(
    "/transaction/{transaction_id}",
    response_model=TransactionResponse,
    status_code=HTTPStatus.OK,
)
def update_transaction(transaction_id: UUID, transaction_data: TransactionData):
    transaction = session.query(Transaction).get(transaction_id)
    transaction.amount = transaction_data.amount
    transaction.date = transaction_data.date
    transaction.type = transaction_data.type

    session.commit()

    return transaction


@router.delete(
    "/transaction/{transaction_id}",
    status_code=HTTPStatus.NO_CONTENT,
)
def delete_transaction(transaction_id: UUID):
    transaction = session.query(Transaction).get(transaction_id)

    if not transaction:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Transaction not found"
        )

    session.delete(transaction)
    session.commit()
    return None