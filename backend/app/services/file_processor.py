import io

import pandas as pd


COLUMN_ALIASES = {
    "transaction_id": ["transaction_id", "txn_id", "id", "transaction id"],
    "date": ["date", "transaction_date", "order_date", "purchase_date"],
    "category": ["category", "spend_category", "product_category"],
    "product": ["product", "product_name", "item", "item_name"],
    "supplier": ["supplier", "supplier_name", "vendor", "vendor_name"],
    "quantity": ["quantity", "qty", "units"],
    "unit_cost": ["unit_cost", "unit price", "unit_price", "price"],
    "total_cost": ["total_cost", "total", "total_spend", "amount", "total amount"],
    "region": ["region", "area", "territory"],
    "warehouse": ["warehouse", "location", "facility"],
    "supplier_name": ["supplier_name", "supplier", "vendor", "vendor_name"],
    "country": ["country", "country_of_origin", "supplier_country"],
    "lead_time": ["lead_time", "lead time", "delivery_days"],
    "contract_value": ["contract_value", "contract value", "contract_amount"],
    "risk_level": ["risk_level", "risk", "risk level"],
    "performance_rating": ["performance_rating", "performance", "rating", "score"],
    "stock_level": ["stock_level", "stock", "current_stock", "on_hand"],
    "reorder_level": ["reorder_level", "reorder", "reorder_point", "min_stock"],
    "inventory_value": ["inventory_value", "inv_value", "stock_value"],
    "budget": ["budget", "budget_amount", "planned_spend"],
    "actual_spend": ["actual_spend", "actual", "spend", "actuals"],
    "variance": ["variance", "budget_variance", "difference"],
}


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    rename_map = {}
    for canonical, aliases in COLUMN_ALIASES.items():
        for col in df.columns:
            if col in aliases and col != canonical:
                rename_map[col] = canonical
                break
    return df.rename(columns=rename_map)


def load_file(content: bytes, filename: str) -> pd.DataFrame:
    if filename.lower().endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content), dtype=str)
    else:
        df = pd.read_excel(io.BytesIO(content), dtype=str)
    return _normalize_columns(df)


def detect_dataset_type(df: pd.DataFrame) -> str | None:
    cols = set(df.columns)
    if cols & {"total_cost", "unit_cost", "transaction_id"}:
        return "procurement"
    if cols & {"risk_level", "performance_rating", "lead_time", "contract_value"}:
        return "supplier"
    if cols & {"stock_level", "reorder_level", "inventory_value"}:
        return "inventory"
    if cols & {"budget", "actual_spend", "variance"}:
        return "budget"
    return None
