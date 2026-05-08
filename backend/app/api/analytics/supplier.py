from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.upload import Upload
from app.models.user import User
from app.schemas.analytics import SupplierSummary
from app.services.analytics.supplier import get_supplier_summary

router = APIRouter()


@router.get("/supplier", response_model=SupplierSummary)
def supplier_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    proc_ids = _ids(db, current_user, "procurement")
    sup_ids = _ids(db, current_user, "supplier")
    return get_supplier_summary(db, proc_ids + sup_ids, {})


def _ids(db: Session, user: User, dataset_type: str) -> list[int]:
    q = db.query(Upload.id).filter(Upload.dataset_type == dataset_type, Upload.status == "valid")
    if user.role != "admin":
        q = q.filter(Upload.user_id == user.id)
    return [row[0] for row in q.all()]
