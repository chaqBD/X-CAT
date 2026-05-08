from sqlalchemy.orm import Session

from app.models.datasets import BudgetRecord, ProcurementTransaction
from app.schemas.analytics import BudgetSummary, KVItem


def get_budget_summary(db: Session, upload_ids: list[int], filters: dict) -> BudgetSummary:
    budget_rows = db.query(BudgetRecord).filter(BudgetRecord.upload_id.in_(upload_ids)).all()
    proc_rows = db.query(ProcurementTransaction).filter(ProcurementTransaction.upload_id.in_(upload_ids)).all()

    actual_by_cat: dict[str, float] = {}
    for r in proc_rows:
        if r.category:
            actual_by_cat[r.category] = actual_by_cat.get(r.category, 0) + (r.total_cost or 0)

    bva = []
    total_budget = 0.0
    total_actual = 0.0
    overspending = []

    for r in budget_rows:
        actual = actual_by_cat.get(r.category, r.actual_spend or 0)
        budget_val = r.budget or 0
        variance = actual - budget_val
        total_budget += budget_val
        total_actual += actual
        bva.append({
            "category": r.category,
            "region": r.region,
            "budget": round(budget_val, 2),
            "actual": round(actual, 2),
            "variance": round(variance, 2),
            "variance_pct": round(variance / budget_val * 100, 2) if budget_val else 0,
        })
        if actual > budget_val:
            overspending.append({"category": r.category, "overspend": round(actual - budget_val, 2)})

    region_spend: dict[str, float] = {}
    for r in proc_rows:
        if r.region:
            region_spend[r.region] = region_spend.get(r.region, 0) + (r.total_cost or 0)

    utilisation = round(total_actual / total_budget * 100, 2) if total_budget else 0

    return BudgetSummary(
        budget_vs_actual=sorted(bva, key=lambda x: -x["budget"]),
        variance_table=sorted(bva, key=lambda x: x["variance"]),
        overspending=sorted(overspending, key=lambda x: -x["overspend"]),
        by_region=[KVItem(name=k, value=round(v, 2)) for k, v in sorted(region_spend.items(), key=lambda x: -x[1])],
        utilisation_pct=utilisation,
    )
