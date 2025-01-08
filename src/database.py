import uuid
from enum import Enum
from sqlalchemy import create_engine, Column, Float, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import sessionmaker, declarative_base


db = create_engine("postgresql://user:password@localhost:5432/db")

Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()


class TransactionType(Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column("amount", Float, nullable=False)
    date = Column("date", DateTime, nullable=False)
    type = Column(SQLAlchemyEnum(TransactionType), nullable=False)

    def _init__(self, amount, date, type):
        self.amount = amount
        self.date = date
        self.type = type


Base.metadata.create_all(bind=db)
