from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.upload import Upload
from app.models.user import User
from app.schemas.analytics import ExecutiveSummary
from app.services.analytics.budget import get_budget_summary
from app.services.analytics.inventory import get_inventory_summary
from app.services.analytics.spend import get_spend_summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/executive", response_model=ExecutiveSummary)
def executive_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    all_ids = _all_ids(db, current_user)
    proc_ids = _ids(db, current_user, "procurement")
    inv_ids = _ids(db, current_user, "inventory")

    spend = get_spend_summary(db, proc_ids, {})
    inventory = get_inventory_summary(db, inv_ids, {})
    budget = get_budget_summary(db, all_ids, {})

    top_category = spend.by_category[0].name if spend.by_category else "N/A"

    return ExecutiveSummary(
        total_spend=spend.total_spend,
        total_transactions=spend.total_transactions,
        total_suppliers=spend.total_suppliers,
        top_category=top_category,
        budget_utilisation_pct=budget.utilisation_pct,
        low_stock_count=inventory.low_stock_count,
        spend_by_category=spend.by_category[:8],
        monthly_trend=spend.monthly_trend,
        top_suppliers=spend.by_supplier[:8],
    )


def _all_ids(db: Session, user: User) -> list[int]:
    q = db.query(Upload.id).filter(Upload.status == "valid")
    if user.role != "admin":
        q = q.filter(Upload.user_id == user.id)
    return [row[0] for row in q.all()]


def _ids(db: Session, user: User, dataset_type: str) -> list[int]:
    q = db.query(Upload.id).filter(Upload.dataset_type == dataset_type, Upload.status == "valid")
    if user.role != "admin":
        q = q.filter(Upload.user_id == user.id)
    return [row[0] for row in q.all()]
