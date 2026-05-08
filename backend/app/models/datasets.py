from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ProcurementTransaction(Base):
    __tablename__ = "procurement_transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    upload_id: Mapped[int] = mapped_column(ForeignKey("uploads.id"), nullable=False, index=True)
    transaction_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    date: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    category: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)
    product: Mapped[str | None] = mapped_column(String(200), nullable=True)
    supplier: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)
    quantity: Mapped[float | None] = mapped_column(Float, nullable=True)
    unit_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    total_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    region: Mapped[str | None] = mapped_column(String(100), nullable=True)
    warehouse: Mapped[str | None] = mapped_column(String(100), nullable=True)

    upload: Mapped["Upload"] = relationship("Upload", back_populates="procurement_rows")


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    upload_id: Mapped[int] = mapped_column(ForeignKey("uploads.id"), nullable=False, index=True)
    supplier_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    lead_time: Mapped[float | None] = mapped_column(Float, nullable=True)
    contract_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    risk_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    performance_rating: Mapped[float | None] = mapped_column(Float, nullable=True)

    upload: Mapped["Upload"] = relationship("Upload", back_populates="supplier_rows")


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    upload_id: Mapped[int] = mapped_column(ForeignKey("uploads.id"), nullable=False, index=True)
    product: Mapped[str | None] = mapped_column(String(200), nullable=True)
    category: Mapped[str | None] = mapped_column(String(200), nullable=True)
    stock_level: Mapped[float | None] = mapped_column(Float, nullable=True)
    reorder_level: Mapped[float | None] = mapped_column(Float, nullable=True)
    warehouse: Mapped[str | None] = mapped_column(String(100), nullable=True)
    inventory_value: Mapped[float | None] = mapped_column(Float, nullable=True)

    upload: Mapped["Upload"] = relationship("Upload", back_populates="inventory_rows")


class BudgetRecord(Base):
    __tablename__ = "budget_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    upload_id: Mapped[int] = mapped_column(ForeignKey("uploads.id"), nullable=False, index=True)
    category: Mapped[str | None] = mapped_column(String(200), nullable=True)
    budget: Mapped[float | None] = mapped_column(Float, nullable=True)
    actual_spend: Mapped[float | None] = mapped_column(Float, nullable=True)
    variance: Mapped[float | None] = mapped_column(Float, nullable=True)
    region: Mapped[str | None] = mapped_column(String(100), nullable=True)

    upload: Mapped["Upload"] = relationship("Upload", back_populates="budget_rows")
