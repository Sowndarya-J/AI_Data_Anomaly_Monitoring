import os
import mysql.connector
import pandas as pd


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "testpassword"),
    "database": os.getenv("DB_NAME", "ecommerce_db"),
}


CSV_FILE = "data/transactions.csv"


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


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
        "quantity",
        "unit_price",
        "total_amount",
    ]

    for column in required_columns:
        assert column in df.columns


def test_database_table_exists():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SHOW TABLES LIKE 'transactions'
    """)

    table = cursor.fetchone()

    cursor.close()
    connection.close()

    assert table is not None


def test_database_record_count():
    df = pd.read_csv(CSV_FILE)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
    """)

    database_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    assert database_count == len(df)


def test_transaction_amounts_are_valid():
    df = pd.read_csv(CSV_FILE)

    calculated_total = df["quantity"] * df["unit_price"]

    difference = (
        df["total_amount"] - calculated_total
    ).abs()

    assert (difference <= 0.01).all()