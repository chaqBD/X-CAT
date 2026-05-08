from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.upload import Upload
from app.models.user import User
from app.schemas.analytics import CategorySummary
from app.services.analytics.category import get_category_summary

router = APIRouter()


@router.get("/category", response_model=CategorySummary)
def category_analysis(
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    proc_ids = _ids(db, current_user, "procurement")
    budget_ids = _ids(db, current_user, "budget")
    return get_category_summary(db, proc_ids + budget_ids, {"date_from": date_from, "date_to": date_to})


def _ids(db: Session, user: User, dataset_type: str) -> list[int]:
    q = db.query(Upload.id).filter(Upload.dataset_type == dataset_type, Upload.status == "valid")
    if user.role != "admin":
        q = q.filter(Upload.user_id == user.id)
    return [row[0] for row in q.all()]
