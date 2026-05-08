import json

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.core.config import settings
from app.core.database import get_db
from app.models.datasets import BudgetRecord, InventoryItem, ProcurementTransaction, Supplier
from app.models.upload import Upload
from app.models.user import User
from app.schemas.upload import UploadOut, ValidationResult
from app.services.file_processor import detect_dataset_type, load_file
from app.services.validator import clean, validate

router = APIRouter(prefix="/uploads", tags=["uploads"])

MAX_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024


@router.post("/", response_model=UploadOut, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    dataset_type: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "analyst")),
):
    content = await file.read()
    if len(content) > MAX_BYTES:
        raise HTTPException(400, detail=f"File exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit")

    filename = file.filename or "upload"
    if not (filename.lower().endswith(".csv") or filename.lower().endswith(".xlsx") or filename.lower().endswith(".xls")):
        raise HTTPException(400, detail="Only CSV and Excel files are supported")

    try:
        df = load_file(content, filename)
    except Exception as e:
        raise HTTPException(400, detail=f"Could not parse file: {e}")

    if not dataset_type:
        dataset_type = detect_dataset_type(df)
    if not dataset_type:
        raise HTTPException(400, detail="Could not detect dataset type. Please specify it manually.")

    result = validate(df, dataset_type)

    upload = Upload(
        user_id=current_user.id,
        filename=filename,
        dataset_type=dataset_type,
        status="invalid" if not result.valid else "valid",
        row_count=result.row_count,
        error_log=json.dumps({"errors": result.errors, "warnings": result.warnings}) if (result.errors or result.warnings) else None,
    )
    db.add(upload)
    db.flush()

    if result.valid:
        df_clean = clean(df, dataset_type)
        _store_rows(db, df_clean, dataset_type, upload.id)

    db.commit()
    db.refresh(upload)
    return upload


@router.get("/", response_model=list[UploadOut])
def list_uploads(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    q = db.query(Upload)
    if current_user.role != "admin":
        q = q.filter(Upload.user_id == current_user.id)
    return q.order_by(Upload.created_at.desc()).all()


@router.get("/{upload_id}", response_model=UploadOut)
def get_upload(upload_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    upload = db.query(Upload).filter(Upload.id == upload_id).first()
    if not upload:
        raise HTTPException(404, detail="Upload not found")
    if current_user.role != "admin" and upload.user_id != current_user.id:
        raise HTTPException(403, detail="Access denied")
    return upload


@router.delete("/{upload_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_upload(upload_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles("admin", "analyst"))):
    upload = db.query(Upload).filter(Upload.id == upload_id).first()
    if not upload:
        raise HTTPException(404, detail="Upload not found")
    if current_user.role != "admin" and upload.user_id != current_user.id:
        raise HTTPException(403, detail="Access denied")
    db.delete(upload)
    db.commit()


def _store_rows(db: Session, df, dataset_type: str, upload_id: int):
    rows = df.where(df.notna(), other=None).to_dict(orient="records")
    if dataset_type == "procurement":
        db.bulk_insert_mappings(ProcurementTransaction, [{"upload_id": upload_id, **r} for r in rows])
    elif dataset_type == "supplier":
        db.bulk_insert_mappings(Supplier, [{"upload_id": upload_id, **r} for r in rows])
    elif dataset_type == "inventory":
        db.bulk_insert_mappings(InventoryItem, [{"upload_id": upload_id, **r} for r in rows])
    elif dataset_type == "budget":
        db.bulk_insert_mappings(BudgetRecord, [{"upload_id": upload_id, **r} for r in rows])
