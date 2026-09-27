import pandas as pd


REQUIRED_COLUMNS = [
    "transaction_id",
    "date",
    "customer_id",
    "product_id",
    "quantity",
    "unit_price",
    "payment_method",
    "total_amount"
]


def load_data(file_path):
    """Load raw transaction data."""
    df = pd.read_csv(file_path)
    return df


def check_required_columns(df):
    """Check whether all required columns exist."""

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        return False, missing_columns

    return True, []


def check_missing_values(df):
    """Check for missing values."""

    missing_values = df.isnull().sum()

    missing_values = missing_values[
        missing_values > 0
    ]

    return missing_values.to_dict()


def check_duplicate_transactions(df):
    """Check duplicate transaction IDs."""

    duplicate_count = df["transaction_id"].duplicated().sum()

    return int(duplicate_count)


def check_invalid_quantity(df):
    """Check for zero or negative quantities."""

    invalid_count = (
        df["quantity"] <= 0
    ).sum()

    return int(invalid_count)


def check_invalid_price(df):
    """Check for zero or negative prices."""

    invalid_count = (
        df["unit_price"] <= 0
    ).sum()

    return int(invalid_count)


def check_negative_amount(df):
    """Check for negative transaction amounts."""

    invalid_count = (
        df["total_amount"] < 0
    ).sum()

    return int(invalid_count)


def check_date_format(df):
    """Check whether transaction dates are valid."""

    converted_dates = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    invalid_count = converted_dates.isnull().sum()

    return int(invalid_count)


def run_data_quality_checks(df):

    results = {}

    # Required columns
    columns_valid, missing_columns = (
        check_required_columns(df)
    )

    results["required_columns"] = {
        "status": columns_valid,
        "missing_columns": missing_columns
    }

    # Missing values
    results["missing_values"] = (
        check_missing_values(df)
    )

    # Duplicate IDs
    results["duplicate_transactions"] = (
        check_duplicate_transactions(df)
    )

    # Quantity
    results["invalid_quantity"] = (
        check_invalid_quantity(df)
    )

    # Price
    results["invalid_price"] = (
        check_invalid_price(df)
    )

    # Amount
    results["negative_amount"] = (
        check_negative_amount(df)
    )

    # Date
    results["invalid_dates"] = (
        check_date_format(df)
    )

    return results


if __name__ == "__main__":

    file_path = (
        "data/raw/ecommerce_transactions.csv"
    )

    df = load_data(file_path)

    results = run_data_quality_checks(df)

    print("\n================================")
    print("     DATA QUALITY REPORT")
    print("================================")

    print(
        "\nRequired Columns:",
        results["required_columns"]
    )

    print(
        "\nMissing Values:",
        results["missing_values"]
    )

    print(
        "\nDuplicate Transactions:",
        results["duplicate_transactions"]
    )

    print(
        "\nInvalid Quantity:",
        results["invalid_quantity"]
    )

    print(
        "\nInvalid Price:",
        results["invalid_price"]
    )

    print(
        "\nNegative Amount:",
        results["negative_amount"]
    )

    print(
        "\nInvalid Dates:",
        results["invalid_dates"]
    )