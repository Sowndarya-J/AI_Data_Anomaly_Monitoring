import pandas as pd
from pathlib import Path


# ==========================================
# FILE PATHS
# ==========================================

RAW_FILE = Path(
    "data/raw/ecommerce_transactions.csv"
)

PROCESSED_FILE = Path(
    "data/processed/ecommerce_transactions_clean.csv"
)


# ==========================================
# EXTRACT
# ==========================================

def extract_data():
    """
    Read raw CSV data.
    """

    print("\n[EXTRACT] Reading raw data...")

    df = pd.read_csv(RAW_FILE)

    print(
        f"[EXTRACT] Records loaded: {len(df)}"
    )

    return df


# ==========================================
# TRANSFORM
# ==========================================

def transform_data(df):
    """
    Clean and transform transaction data.
    """

    print("\n[TRANSFORM] Cleaning data...")

    # Convert date column
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    # Remove duplicate transaction IDs
    before_duplicates = len(df)

    df = df.drop_duplicates(
        subset=["transaction_id"],
        keep="first"
    )

    duplicates_removed = (
        before_duplicates - len(df)
    )

    print(
        f"[TRANSFORM] Duplicates removed: "
        f"{duplicates_removed}"
    )

    # Remove invalid quantities
    before_quantity = len(df)

    df = df[df["quantity"] > 0]

    quantity_removed = (
        before_quantity - len(df)
    )

    print(
        f"[TRANSFORM] Invalid quantities removed: "
        f"{quantity_removed}"
    )

    # Remove invalid prices
    before_price = len(df)

    df = df[df["unit_price"] > 0]

    price_removed = (
        before_price - len(df)
    )

    print(
        f"[TRANSFORM] Invalid prices removed: "
        f"{price_removed}"
    )

    # Remove negative transaction amounts
    before_amount = len(df)

    df = df[df["total_amount"] >= 0]

    amount_removed = (
        before_amount - len(df)
    )

    print(
        f"[TRANSFORM] Negative amounts removed: "
        f"{amount_removed}"
    )

    # Recalculate total amount
    df["total_amount"] = (
        df["quantity"] * df["unit_price"]
    ).round(2)

    # Sort by date
    df = df.sort_values(
        by="date"
    )

    # Reset index
    df = df.reset_index(
        drop=True
    )

    print(
        f"[TRANSFORM] Final records: {len(df)}"
    )

    return df


# ==========================================
# LOAD
# ==========================================

def load_data(df):
    """
    Save cleaned data.
    """

    print("\n[LOAD] Saving processed data...")

    PROCESSED_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        PROCESSED_FILE,
        index=False
    )

    print(
        f"[LOAD] File saved: {PROCESSED_FILE}"
    )


# ==========================================
# MAIN ETL PIPELINE
# ==========================================

def run_etl():

    print("\n====================================")
    print("        ETL PIPELINE STARTED")
    print("====================================")

    # Extract
    df = extract_data()

    # Transform
    df = transform_data(df)

    # Load
    load_data(df)

    print("\n====================================")
    print("        ETL PIPELINE COMPLETED")
    print("====================================")


if __name__ == "__main__":
    run_etl()