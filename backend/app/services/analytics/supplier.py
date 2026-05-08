from sqlalchemy.orm import Session

from app.models.datasets import ProcurementTransaction, Supplier
from app.schemas.analytics import KVItem, SupplierSummary


def get_supplier_summary(db: Session, upload_ids: list[int], filters: dict) -> SupplierSummary:
    proc_rows = db.query(ProcurementTransaction).filter(ProcurementTransaction.upload_id.in_(upload_ids)).all()
    sup_rows = db.query(Supplier).filter(Supplier.upload_id.in_(upload_ids)).all()

    sup_spend: dict[str, float] = {}
    for r in proc_rows:
        if r.supplier:
            sup_spend[r.supplier] = sup_spend.get(r.supplier, 0) + (r.total_cost or 0)

    total = sum(sup_spend.values()) or 1
    concentration = [KVItem(name=k, value=round(v / total * 100, 2)) for k, v in sorted(sup_spend.items(), key=lambda x: -x[1])[:10]]

    lead_time_avg: dict[str, list[float]] = {}
    risk_count: dict[str, int] = {}
    for s in sup_rows:
        if s.supplier_name and s.lead_time is not None:
            lead_time_avg.setdefault(s.supplier_name, []).append(s.lead_time)
        if s.risk_level:
            risk_count[s.risk_level] = risk_count.get(s.risk_level, 0) + 1

    lt_items = [KVItem(name=k, value=round(sum(v) / len(v), 2)) for k, v in lead_time_avg.items()]
    lt_items.sort(key=lambda x: -x.value)

    return SupplierSummary(
        rankings=[KVItem(name=k, value=round(v, 2)) for k, v in sorted(sup_spend.items(), key=lambda x: -x[1])[:20]],
        concentration=concentration,
        lead_time_avg=lt_items[:20],
        risk_breakdown=[KVItem(name=k, value=float(v)) for k, v in sorted(risk_count.items())],
    )
