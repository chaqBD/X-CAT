import pandas as pd

from app.schemas.upload import ValidationResult

REQUIRED_COLUMNS = {
    "procurement": ["date", "category", "supplier", "total_cost"],
    "supplier": ["supplier_name", "country"],
    "inventory": ["product", "stock_level", "reorder_level"],
    "budget": ["category", "budget", "actual_spend"],
}

NUMERIC_COLUMNS = {
    "procurement": ["quantity", "unit_cost", "total_cost"],
    "supplier": ["lead_time", "contract_value", "performance_rating"],
    "inventory": ["stock_level", "reorder_level", "inventory_value"],
    "budget": ["budget", "actual_spend", "variance"],
}


def validate(df: pd.DataFrame, dataset_type: str) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    required = REQUIRED_COLUMNS.get(dataset_type, [])
    missing = [c for c in required if c not in df.columns]
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")

    numeric_cols = NUMERIC_COLUMNS.get(dataset_type, [])
    for col in numeric_cols:
        if col in df.columns:
            coerced = pd.to_numeric(df[col], errors="coerce")
            bad = coerced.isna() & df[col].notna()
            if bad.any():
                errors.append(f"Column '{col}' has {bad.sum()} non-numeric value(s)")

    if dataset_type == "procurement" and "date" in df.columns:
        parsed = pd.to_datetime(df["date"], errors="coerce")
        bad_dates = parsed.isna() & df["date"].notna()
        if bad_dates.any():
            errors.append(f"Column 'date' has {bad_dates.sum()} unparseable date(s)")

    dup_count = df.duplicated().sum()
    if dup_count > 0:
        warnings.append(f"{dup_count} duplicate row(s) detected and will be removed")

    null_pcts = df.isnull().mean()
    for col in required:
        if col in null_pcts and null_pcts[col] > 0:
            warnings.append(f"Column '{col}' has {null_pcts[col]:.0%} missing values")

    return ValidationResult(
        valid=len(errors) == 0,
        row_count=len(df),
        errors=errors,
        warnings=warnings,
    )


def clean(df: pd.DataFrame, dataset_type: str) -> pd.DataFrame:
    df = df.drop_duplicates()
    numeric_cols = NUMERIC_COLUMNS.get(dataset_type, [])
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if dataset_type == "procurement" and "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    return df
