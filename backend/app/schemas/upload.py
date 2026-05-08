from datetime import datetime

from pydantic import BaseModel


class UploadOut(BaseModel):
    id: int
    filename: str
    dataset_type: str
    status: str
    row_count: int
    error_log: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ValidationResult(BaseModel):
    valid: bool
    row_count: int
    errors: list[str]
    warnings: list[str]
