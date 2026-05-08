from sqlalchemy.orm import Session

from app.models.datasets import ProcurementTransaction
from app.schemas.analytics import KVItem, SpendSummary, TrendPoint


def get_spend_summary(db: Session, upload_ids: list[int], filters: dict) -> SpendSummary:
    q = db.query(ProcurementTransaction).filter(ProcurementTransaction.upload_id.in_(upload_ids))

    if filters.get("date_from"):
        q = q.filter(ProcurementTransaction.date >= filters["date_from"])
    if filters.get("date_to"):
        q = q.filter(ProcurementTransaction.date <= filters["date_to"])
    if filters.get("category"):
        q = q.filter(ProcurementTransaction.category.in_(filters["category"]))
    if filters.get("supplier"):
        q = q.filter(ProcurementTransaction.supplier.in_(filters["supplier"]))

    rows = q.all()

    total_spend = sum(r.total_cost or 0 for r in rows)
    total_transactions = len(rows)
    suppliers = {r.supplier for r in rows if r.supplier}

    cat_spend: dict[str, float] = {}
    sup_spend: dict[str, float] = {}
    month_spend: dict[str, float] = {}
    prod_spend: dict[str, float] = {}

    for r in rows:
        cost = r.total_cost or 0
        if r.category:
            cat_spend[r.category] = cat_spend.get(r.category, 0) + cost
        if r.supplier:
            sup_spend[r.supplier] = sup_spend.get(r.supplier, 0) + cost
        if r.date:
            key = r.date.strftime("%Y-%m")
            month_spend[key] = month_spend.get(key, 0) + cost
        if r.product:
            prod_spend[r.product] = prod_spend.get(r.product, 0) + cost

    return SpendSummary(
        total_spend=round(total_spend, 2),
        total_transactions=total_transactions,
        total_suppliers=len(suppliers),
        by_category=_top(cat_spend, 20),
        by_supplier=_top(sup_spend, 20),
        monthly_trend=_trend(month_spend),
        top_products=_top(prod_spend, 10),
    )


def _top(d: dict, n: int) -> list[KVItem]:
    return [KVItem(name=k, value=round(v, 2)) for k, v in sorted(d.items(), key=lambda x: -x[1])[:n]]


def _trend(d: dict) -> list[TrendPoint]:
    return [TrendPoint(period=k, value=round(v, 2)) for k, v in sorted(d.items())]
