import pandas as pd
import mysql.connector
import pytest


CSV_FILE = "data/processed/ecommerce_transactions_clean.csv"

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "#Sownd@1710#",
    "database": "anomaly_monitoring"
}


@pytest.fixture
def db_connection():
    connection = mysql.connector.connect(**DB_CONFIG)

    yield connection

    connection.close()


def test_csv_file_exists():
    df = pd.read_csv(CSV_FILE)

    assert len(df) > 0


def test_required_columns_exist():
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


def test_csv_and_database_record_count_match(db_connection):
    df = pd.read_csv(CSV_FILE)

    csv_count = len(df)

    cursor = db_connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    )

    database_count = cursor.fetchone()[0]

    cursor.close()

    assert csv_count == database_count


def test_csv_total_amount_calculation():
    df = pd.read_csv(CSV_FILE)

    calculated_total = (
        df["quantity"] * df["unit_price"]
    )

    difference = (
        df["total_amount"] - calculated_total
    ).abs()

    assert (difference <= 0.01).all()


def test_required_fields_not_null():
    df = pd.read_csv(CSV_FILE)

    required_columns = [
        "transaction_id",
        "date",
        "customer_id",
        "product_id",
        "quantity",
        "unit_price",
        "total_amount"
    ]

    for column in required_columns:
        assert df[column].isnull().sum() == 0