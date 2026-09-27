import pandas as pd


CSV_FILE = "data/processed/ecommerce_transactions_clean.csv"


def load_data():
    return pd.read_csv(CSV_FILE)


def calculate_total(quantity, unit_price):
    return quantity * unit_price


def validate_transaction(row):
    if row["quantity"] <= 0:
        return False

    if row["unit_price"] <= 0:
        return False

    if pd.isna(row["transaction_id"]):
        return False

    return True


def test_load_data():
    df = load_data()

    assert df is not None
    assert len(df) > 0


def test_calculate_total():
    result = calculate_total(5, 100)

    assert result == 500


def test_calculate_total_decimal():
    result = calculate_total(3, 99.50)

    assert result == 298.50


def test_valid_transaction():
    transaction = {
        "transaction_id": "TX001",
        "quantity": 2,
        "unit_price": 150.00
    }

    assert validate_transaction(transaction) is True


def test_invalid_quantity():
    transaction = {
        "transaction_id": "TX002",
        "quantity": 0,
        "unit_price": 150.00
    }

    assert validate_transaction(transaction) is False


def test_invalid_price():
    transaction = {
        "transaction_id": "TX003",
        "quantity": 2,
        "unit_price": 0
    }

    assert validate_transaction(transaction) is False