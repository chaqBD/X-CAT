from sqlalchemy.orm import Session

from app.models.datasets import InventoryItem
from app.schemas.analytics import InventorySummary, KVItem


def get_inventory_summary(db: Session, upload_ids: list[int], filters: dict) -> InventorySummary:
    rows = db.query(InventoryItem).filter(InventoryItem.upload_id.in_(upload_ids)).all()

    stock_levels = [KVItem(name=r.product or "Unknown", value=r.stock_level or 0) for r in rows if r.product]
    stock_levels.sort(key=lambda x: -x.value)

    low_stock = [
        {"product": r.product, "category": r.category, "stock_level": r.stock_level, "reorder_level": r.reorder_level, "warehouse": r.warehouse}
        for r in rows
        if r.stock_level is not None and r.reorder_level is not None and r.stock_level <= r.reorder_level
    ]

    overstock = [
        {"product": r.product, "category": r.category, "stock_level": r.stock_level, "reorder_level": r.reorder_level, "warehouse": r.warehouse}
        for r in rows
        if r.stock_level is not None and r.reorder_level is not None and r.stock_level >= r.reorder_level * 3
    ]

    wh_value: dict[str, float] = {}
    for r in rows:
        if r.warehouse:
            wh_value[r.warehouse] = wh_value.get(r.warehouse, 0) + (r.inventory_value or 0)

    return InventorySummary(
        stock_levels=stock_levels[:30],
        low_stock=low_stock,
        overstock=overstock,
        by_warehouse=[KVItem(name=k, value=round(v, 2)) for k, v in sorted(wh_value.items(), key=lambda x: -x[1])],
        low_stock_count=len(low_stock),
    )
