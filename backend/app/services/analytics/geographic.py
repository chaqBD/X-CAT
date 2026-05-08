from sqlalchemy.orm import Session

from app.models.datasets import ProcurementTransaction, Supplier
from app.schemas.analytics import GeographicSummary, KVItem


def get_geographic_summary(db: Session, upload_ids: list[int], filters: dict) -> GeographicSummary:
    proc_rows = db.query(ProcurementTransaction).filter(ProcurementTransaction.upload_id.in_(upload_ids)).all()
    sup_rows = db.query(Supplier).filter(Supplier.upload_id.in_(upload_ids)).all()

    region_spend: dict[str, float] = {}
    region_tx: dict[str, int] = {}
    for r in proc_rows:
        if r.region:
            region_spend[r.region] = region_spend.get(r.region, 0) + (r.total_cost or 0)
            region_tx[r.region] = region_tx.get(r.region, 0) + 1

    country_count: dict[str, int] = {}
    for s in sup_rows:
        if s.country:
            country_count[s.country] = country_count.get(s.country, 0) + 1

    regional_activity = [
        {"region": r, "total_spend": round(region_spend[r], 2), "transactions": region_tx.get(r, 0)}
        for r in sorted(region_spend, key=lambda x: -region_spend[x])
    ]

    return GeographicSummary(
        spend_by_region=[KVItem(name=k, value=round(v, 2)) for k, v in sorted(region_spend.items(), key=lambda x: -x[1])],
        suppliers_by_country=[KVItem(name=k, value=float(v)) for k, v in sorted(country_count.items(), key=lambda x: -x[1])[:20]],
        regional_activity=regional_activity,
    )
