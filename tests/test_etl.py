import os
import mysql.connector
import pandas as pd
import pytest


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "testpassword"),
    "database": os.getenv("DB_NAME", "ecommerce_db"),
}


CSV_FILE = "data/transactions.csv"


@pytest.fixture
def db_connection():
    connection = mysql.connector.connect(**DB_CONFIG)

    yield connection

    connection.close()


def test_csv_file_exists():
    assert os.path.exists(CSV_FILE)


def test_required_columns_exist():
    df = pd.read_csv(CSV_FILE)

    required_columns = [
        "transaction_id",
        "quantity",
        "unit_price",
        "total_amount",
    ]

    for column in required_columns:
        assert column in df.columns


def test_csv_and_database_record_count_match(db_connection):
    df = pd.read_csv(CSV_FILE)

    cursor = db_connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM transactions")

    database_count = cursor.fetchone()[0]

    cursor.close()

    assert len(df) == database_count


def test_csv_total_amount_calculation():
    df = pd.read_csv(CSV_FILE)

    calculated_total = df["quantity"] * df["unit_price"]

    difference = (df["total_amount"] - calculated_total).abs()

    assert (difference <= 0.01).all()


def test_required_fields_not_null():
    df = pd.read_csv(CSV_FILE)

    required_columns = [
        "transaction_id",
        "quantity",
        "unit_price",
        "total_amount",
    ]

    assert not df[required_columns].isnull().any().any()