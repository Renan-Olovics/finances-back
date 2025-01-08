from fastapi import FastAPI

from http import HTTPStatus


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
