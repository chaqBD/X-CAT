import csv
import io

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.datasets import BudgetRecord, InventoryItem, ProcurementTransaction, Supplier
from app.models.upload import Upload
from app.models.user import User

router = APIRouter(prefix="/exports", tags=["exports"])

DATASET_MODEL_MAP = {
    "procurement": (ProcurementTransaction, ["transaction_id", "date", "category", "product", "supplier", "quantity", "unit_cost", "total_cost", "region", "warehouse"]),
    "supplier": (Supplier, ["supplier_name", "country", "lead_time", "contract_value", "risk_level", "performance_rating"]),
    "inventory": (InventoryItem, ["product", "category", "stock_level", "reorder_level", "warehouse", "inventory_value"]),
    "budget": (BudgetRecord, ["category", "budget", "actual_spend", "variance", "region"]),
}


@router.get("/csv/{dataset_type}")
def export_csv(
    dataset_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if dataset_type not in DATASET_MODEL_MAP:
        raise HTTPException(400, detail=f"Unknown dataset type: {dataset_type}")

    model, fields = DATASET_MODEL_MAP[dataset_type]
    q = db.query(model).join(Upload, model.upload_id == Upload.id).filter(Upload.status == "valid")
    if current_user.role != "admin":
        q = q.filter(Upload.user_id == current_user.id)

    rows = q.all()
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow({f: getattr(row, f, None) for f in fields})

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=xcat_{dataset_type}.csv"},
    )
