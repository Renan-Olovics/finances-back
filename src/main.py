from fastapi import FastAPI

from src.router import transaction


app = FastAPI()


app.include_router(transaction.router)
