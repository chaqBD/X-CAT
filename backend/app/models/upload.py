from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

DATASET_TYPES = ("procurement", "supplier", "inventory", "budget")
UPLOAD_STATUSES = ("pending", "processing", "valid", "invalid")


class Upload(Base):
    __tablename__ = "uploads"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    dataset_type: Mapped[str] = mapped_column(Enum(*DATASET_TYPES, name="dataset_type"), nullable=False)
    status: Mapped[str] = mapped_column(Enum(*UPLOAD_STATUSES, name="upload_status"), default="pending")
    row_count: Mapped[int] = mapped_column(Integer, default=0)
    error_log: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship("User", back_populates="uploads")
    procurement_rows: Mapped[list["ProcurementTransaction"]] = relationship("ProcurementTransaction", back_populates="upload", cascade="all, delete-orphan")
    supplier_rows: Mapped[list["Supplier"]] = relationship("Supplier", back_populates="upload", cascade="all, delete-orphan")
    inventory_rows: Mapped[list["InventoryItem"]] = relationship("InventoryItem", back_populates="upload", cascade="all, delete-orphan")
    budget_rows: Mapped[list["BudgetRecord"]] = relationship("BudgetRecord", back_populates="upload", cascade="all, delete-orphan")
