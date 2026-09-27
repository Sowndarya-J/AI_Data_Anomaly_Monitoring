import pandas as pd
import mysql.connector


CSV_FILE = "data/processed/ecommerce_transactions_clean.csv"

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "#Sownd@1710#",
    "database": "anomaly_monitoring"
}


def test_csv_still_has_data():
    df = pd.read_csv(CSV_FILE)

    assert len(df) > 0


def test_transaction_id_is_unique():
    df = pd.read_csv(CSV_FILE)

    assert df["transaction_id"].is_unique


def test_required_columns_still_exist():
    df = pd.read_csv(CSV_FILE)

    required_columns = [
        "transaction_id",
        "date",
        "customer_id",
        "product_id",
        "quantity",
        "unit_price",
        "payment_method",
        "total_amount"
    ]

    for column in required_columns:
        assert column in df.columns


def test_database_table_exists():
    connection = mysql.connector.connect(**DB_CONFIG)

    cursor = connection.cursor()

    cursor.execute(
        """
        SHOW TABLES LIKE 'transactions'
        """
    )

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    assert result is not None


def test_database_record_count():
    connection = mysql.connector.connect(**DB_CONFIG)

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    )

    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    assert count > 0


def test_transaction_amounts_are_valid():
    df = pd.read_csv(CSV_FILE)

    calculated_total = (
        df["quantity"] * df["unit_price"]
    )

    difference = (
        df["total_amount"] - calculated_total
    ).abs()

    assert (difference <= 0.01).all()