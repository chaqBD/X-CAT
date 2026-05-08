from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.upload import Upload
from app.models.user import User
from app.schemas.analytics import SpendSummary
from app.services.analytics.spend import get_spend_summary

router = APIRouter()


@router.get("/spend", response_model=SpendSummary)
def spend_analysis(
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    category: list[str] | None = Query(None),
    supplier: list[str] | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    upload_ids = _get_upload_ids(db, current_user, "procurement")
    return get_spend_summary(db, upload_ids, {"date_from": date_from, "date_to": date_to, "category": category, "supplier": supplier})


def _get_upload_ids(db: Session, user: User, dataset_type: str) -> list[int]:
    q = db.query(Upload.id).filter(Upload.dataset_type == dataset_type, Upload.status == "valid")
    if user.role != "admin":
        q = q.filter(Upload.user_id == user.id)
    return [row[0] for row in q.all()]
