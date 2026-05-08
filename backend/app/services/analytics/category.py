from sqlalchemy.orm import Session

from app.models.datasets import BudgetRecord, ProcurementTransaction
from app.schemas.analytics import CategorySummary, KVItem


def get_category_summary(db: Session, upload_ids: list[int], filters: dict) -> CategorySummary:
    q = db.query(ProcurementTransaction).filter(ProcurementTransaction.upload_id.in_(upload_ids))
    if filters.get("date_from"):
        q = q.filter(ProcurementTransaction.date >= filters["date_from"])
    if filters.get("date_to"):
        q = q.filter(ProcurementTransaction.date <= filters["date_to"])

    rows = q.all()

    cat_spend: dict[str, float] = {}
    cat_month: dict[str, dict[str, float]] = {}
    for r in rows:
        if not r.category:
            continue
        cost = r.total_cost or 0
        cat_spend[r.category] = cat_spend.get(r.category, 0) + cost
        if r.date:
            m = r.date.strftime("%Y-%m")
            cat_month.setdefault(r.category, {})
            cat_month[r.category][m] = cat_month[r.category].get(m, 0) + cost

    total = sum(cat_spend.values()) or 1
    contribution = [KVItem(name=k, value=round(v / total * 100, 2)) for k, v in sorted(cat_spend.items(), key=lambda x: -x[1])]

    budget_rows = db.query(BudgetRecord).filter(BudgetRecord.upload_id.in_(upload_ids)).all()
    budget_map: dict[str, float] = {r.category: (r.budget or 0) for r in budget_rows if r.category}
    utilisation = []
    for cat, spend in cat_spend.items():
        bud = budget_map.get(cat, 0)
        if bud > 0:
            utilisation.append(KVItem(name=cat, value=round(spend / bud * 100, 2)))

    mom_growth = _compute_mom(cat_month)

    return CategorySummary(
        rankings=[KVItem(name=k, value=round(v, 2)) for k, v in sorted(cat_spend.items(), key=lambda x: -x[1])[:20]],
        budget_utilisation=utilisation,
        contribution=contribution[:20],
        mom_growth=mom_growth,
    )


def _compute_mom(cat_month: dict[str, dict[str, float]]) -> list[KVItem]:
    results = []
    for cat, months in cat_month.items():
        sorted_months = sorted(months.keys())
        if len(sorted_months) >= 2:
            prev = months[sorted_months[-2]] or 1
            curr = months[sorted_months[-1]]
            growth = (curr - prev) / prev * 100
            results.append(KVItem(name=cat, value=round(growth, 2)))
    return sorted(results, key=lambda x: -x.value)[:20]
