from fastapi import FastAPI, Query, HTTPException

from http import HTTPStatus

from uuid import UUID


from src.database import Transaction, session

from src.models import TransactionResponse, TransactionData

app = FastAPI()


@app.post(
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


@app.get(
    "/transaction/{transaction_id}",
    response_model=TransactionResponse,
    status_code=HTTPStatus.OK,
)
def read_transaction(transaction_id: UUID):
    transaction = session.query(Transaction).get(transaction_id)
    return transaction


@app.get(
    "/transaction",
    response_model=list[TransactionResponse],
    status_code=HTTPStatus.OK,
)
def read_transactions(limit: UUID = Query(10, le=100), offset: int = Query(0, ge=0)):
    transactions = session.query(Transaction).offset(offset).limit(limit).all()
    return transactions
