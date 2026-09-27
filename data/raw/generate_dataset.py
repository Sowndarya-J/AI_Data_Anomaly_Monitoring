import pandas as pd
import numpy as np

# For reproducible results
np.random.seed(42)

# Number of transactions
n = 1000

# Create normal transaction data
data = {
    "transaction_id": [f"T{i:04d}" for i in range(1, n + 1)],

    "date": pd.date_range(
        start="2026-01-01",
        periods=n,
        freq="h"
    ),

    "customer_id": [
        f"C{np.random.randint(1001, 1200)}"
        for _ in range(n)
    ],

    "product_id": [
        f"P{np.random.randint(101, 151)}"
        for _ in range(n)
    ],

    "quantity": np.random.randint(1, 6, n),

    "unit_price": np.random.uniform(
        100, 5000, n
    ).round(2),

    "payment_method": np.random.choice(
        ["UPI", "Credit Card", "Debit Card", "Net Banking"],
        n
    )
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Calculate transaction amount
df["total_amount"] = (
    df["quantity"] * df["unit_price"]
).round(2)


# ==========================================
# ADD INTENTIONAL ANOMALIES
# ==========================================

# Anomaly 1: Very high quantity
df.loc[100, "quantity"] = 100

df.loc[100, "total_amount"] = (
    df.loc[100, "quantity"]
    * df.loc[100, "unit_price"]
)


# Anomaly 2: Very high unit price
df.loc[250, "unit_price"] = 50000

df.loc[250, "total_amount"] = (
    df.loc[250, "quantity"]
    * df.loc[250, "unit_price"]
)


# Anomaly 3: Extremely large transaction
df.loc[500, "quantity"] = 200
df.loc[500, "unit_price"] = 75000

df.loc[500, "total_amount"] = (
    df.loc[500, "quantity"]
    * df.loc[500, "unit_price"]
)


# Anomaly 4: Negative transaction amount
df.loc[750, "total_amount"] = -5000


# Anomaly 5: Duplicate transaction ID
df.loc[900, "transaction_id"] = (
    df.loc[899, "transaction_id"]
)


# ==========================================
# SAVE DATASET
# ==========================================

output_path = "data/raw/ecommerce_transactions.csv"

df.to_csv(
    output_path,
    index=False
)

print("======================================")
print("Dataset created successfully!")
print("======================================")
print(f"Total records : {len(df)}")
print(f"Total columns : {len(df.columns)}")
print(f"Saved to      : {output_path}")