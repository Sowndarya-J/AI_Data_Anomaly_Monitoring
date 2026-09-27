import sys
from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.database.db_connection import get_connection


def load_data():

    query = """
    SELECT
        transaction_id,
        quantity,
        unit_price,
        total_amount
    FROM transactions
    """

    connection = get_connection()

    try:
        df = pd.read_sql(query, connection)
    finally:
        connection.close()

    return df


def detect_anomalies(df):

    features = [
        "quantity",
        "unit_price",
        "total_amount"
    ]

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    df["anomaly_prediction"] = model.fit_predict(
        df[features]
    )

    df["anomaly_status"] = df[
        "anomaly_prediction"
    ].map(
        {
            1: "NORMAL",
            -1: "ANOMALY"
        }
    )

    return df


def generate_anomaly_reasons(df):

    quantity_threshold = df["quantity"].quantile(0.95)
    price_threshold = df["unit_price"].quantile(0.95)
    amount_threshold = df["total_amount"].quantile(0.95)

    reasons = []

    for _, row in df.iterrows():

        transaction_reasons = []

        if row["quantity"] > quantity_threshold:
            transaction_reasons.append(
                "High quantity"
            )

        if row["unit_price"] > price_threshold:
            transaction_reasons.append(
                "High unit price"
            )

        if row["total_amount"] > amount_threshold:
            transaction_reasons.append(
                "High transaction amount"
            )

        if row["anomaly_status"] == "ANOMALY":

            if not transaction_reasons:
                transaction_reasons.append(
                    "Unusual transaction pattern"
                )

            reasons.append(
                ", ".join(transaction_reasons)
            )

        else:
            reasons.append("None")

    df["anomaly_reason"] = reasons

    return df


def main():

    print("Loading transaction data...")

    df = load_data()

    print(
        f"Transactions loaded: {len(df)}"
    )

    print("Running anomaly detection...")

    result = detect_anomalies(df)

    print("Generating anomaly reasons...")

    result = generate_anomaly_reasons(result)

    normal_count = (
        result["anomaly_status"] == "NORMAL"
    ).sum()

    anomaly_count = (
        result["anomaly_status"] == "ANOMALY"
    ).sum()

    print()
    print("========== ANOMALY DETECTION RESULT ==========")
    print(f"Total transactions : {len(result)}")
    print(f"Normal transactions: {normal_count}")
    print(f"Anomalies detected  : {anomaly_count}")
    print("===============================================")

    print()
    print("Sample anomalies:")

    anomalies = result[
        result["anomaly_status"] == "ANOMALY"
    ]

    print(
        anomalies[
            [
                "transaction_id",
                "quantity",
                "unit_price",
                "total_amount",
                "anomaly_reason"
            ]
        ].head(10).to_string(index=False)
    )

    reports_folder = PROJECT_ROOT / "reports"

    reports_folder.mkdir(
        exist_ok=True
    )

    output_file = (
        reports_folder / "anomaly_results.csv"
    )

    result.to_csv(
        output_file,
        index=False
    )

    print()
    print(
        f"Results saved to {output_file}"
    )


if __name__ == "__main__":
    main()