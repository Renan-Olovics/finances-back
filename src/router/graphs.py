from fastapi import APIRouter, Query
from http import HTTPStatus
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import func

from src.database import session, Transaction

router = APIRouter(tags=["Graphs"], prefix="/graphs")


@router.post("/transactions/monthly", status_code=HTTPStatus.OK)
def monthly_transactions(
    monthsBack: int = 12,
    transaction_type: str = Query("ALL", enum=["ALL", "CREDIT", "DEBIT"]),
):
    first_month = datetime.now() - relativedelta(months=monthsBack)

    months = [
        (first_month + relativedelta(months=i))
        .replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        .isoformat()
        for i in range(monthsBack + 1)
    ]

    transaction_filter = session.query(
        func.date_trunc("month", Transaction.date).label("month"),
        func.sum(Transaction.amount).label("total_value"),
    ).filter(Transaction.date >= first_month)

    if transaction_type != "ALL":
        transaction_filter = transaction_filter.filter(
            Transaction.type == transaction_type
        )

    results = (
        transaction_filter.group_by(func.date_trunc("month", Transaction.date))
        .order_by(func.date_trunc("month", Transaction.date))
        .all()
    )

    results_dict = {
        result[0]
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .isoformat(): result[1]
        for result in results
    }

    response = [
        {"month": month, "total": results_dict.get(month, 0)} for month in months
    ]

    return response
