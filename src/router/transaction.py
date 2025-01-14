from fastapi import APIRouter, Query, HTTPException, Depends
from http import HTTPStatus
from uuid import UUID

from src.database import Transaction, session, User
from src.security import get_current_user
from src.models import TransactionResponse, TransactionData

router = APIRouter(tags=["Transaction"], prefix="/transaction")


@router.post("", status_code=HTTPStatus.CREATED, response_model=TransactionResponse)
def create_transaction(
    transaction_data: TransactionData,
    current_user: User = Depends(get_current_user),
):
    print(current_user)
    transaction = Transaction(
        amount=transaction_data.amount,
        date=transaction_data.date,
        type=transaction_data.type,
    )

    session.add(transaction)
    session.commit()

    return transaction


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
    status_code=HTTPStatus.OK,
)
def read_transaction(
    transaction_id: UUID,
    current_user: User = Depends(get_current_user),
):
    if not transaction:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Transaction not found"
        )

    transaction = session.query(Transaction).get(transaction_id)
    return transaction


@router.get(
    "",
    response_model=list[TransactionResponse],
    status_code=HTTPStatus.OK,
)
def read_transactions(
    limit: int = Query(10, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
):
    transactions = session.query(Transaction).offset(offset).limit(limit).all()
    return transactions


@router.put(
    "/{transaction_id}",
    response_model=TransactionResponse,
    status_code=HTTPStatus.OK,
)
def update_transaction(
    transaction_id: UUID,
    transaction_data: TransactionData,
    current_user: User = Depends(get_current_user),
):
    transaction = session.query(Transaction).get(transaction_id)
    transaction.amount = transaction_data.amount
    transaction.date = transaction_data.date
    transaction.type = transaction_data.type

    session.commit()

    return transaction


@router.delete(
    "/{transaction_id}",
    status_code=HTTPStatus.NO_CONTENT,
)
def delete_transaction(
    transaction_id: UUID,
    current_user: User = Depends(get_current_user),
):
    transaction = session.query(Transaction).get(transaction_id)

    if not transaction:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Transaction not found"
        )

    session.delete(transaction)
    session.commit()
    return None
