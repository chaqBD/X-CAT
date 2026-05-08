from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.upload import Upload
from app.models.user import User
from app.schemas.analytics import BudgetSummary
from app.services.analytics.budget import get_budget_summary

router = APIRouter()


@router.get("/budget", response_model=BudgetSummary)
def budget_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    all_ids = _all_ids(db, current_user)
    return get_budget_summary(db, all_ids, {})


def _all_ids(db: Session, user: User) -> list[int]:
    q = db.query(Upload.id).filter(Upload.status == "valid")
    if user.role != "admin":
        q = q.filter(Upload.user_id == user.id)
    return [row[0] for row in q.all()]
