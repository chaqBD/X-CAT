from pydantic import BaseModel


class KVItem(BaseModel):
    name: str
    value: float


class TrendPoint(BaseModel):
    period: str
    value: float


class SpendSummary(BaseModel):
    total_spend: float
    total_transactions: int
    total_suppliers: int
    by_category: list[KVItem]
    by_supplier: list[KVItem]
    monthly_trend: list[TrendPoint]
    top_products: list[KVItem]


class CategorySummary(BaseModel):
    rankings: list[KVItem]
    budget_utilisation: list[KVItem]
    contribution: list[KVItem]
    mom_growth: list[KVItem]


class SupplierSummary(BaseModel):
    rankings: list[KVItem]
    concentration: list[KVItem]
    lead_time_avg: list[KVItem]
    risk_breakdown: list[KVItem]


class InventorySummary(BaseModel):
    stock_levels: list[KVItem]
    low_stock: list[dict]
    overstock: list[dict]
    by_warehouse: list[KVItem]
    low_stock_count: int


class BudgetSummary(BaseModel):
    budget_vs_actual: list[dict]
    variance_table: list[dict]
    overspending: list[dict]
    by_region: list[KVItem]
    utilisation_pct: float


class GeographicSummary(BaseModel):
    spend_by_region: list[KVItem]
    suppliers_by_country: list[KVItem]
    regional_activity: list[dict]


class ExecutiveSummary(BaseModel):
    total_spend: float
    total_transactions: int
    total_suppliers: int
    top_category: str
    budget_utilisation_pct: float
    low_stock_count: int
    spend_by_category: list[KVItem]
    monthly_trend: list[TrendPoint]
    top_suppliers: list[KVItem]
