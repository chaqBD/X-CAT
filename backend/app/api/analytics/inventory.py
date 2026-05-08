from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.upload import Upload
from app.models.user import User
from app.schemas.analytics import InventorySummary
from app.services.analytics.inventory import get_inventory_summary

router = APIRouter()


@router.get("/inventory", response_model=InventorySummary)
def inventory_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ids = _ids(db, current_user)
    return get_inventory_summary(db, ids, {})


def _ids(db: Session, user: User) -> list[int]:
    q = db.query(Upload.id).filter(Upload.dataset_type == "inventory", Upload.status == "valid")
    if user.role != "admin":
        q = q.filter(Upload.user_id == user.id)
    return [row[0] for row in q.all()]
