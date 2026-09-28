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


def test_csv_to_mysql_integration():

    # Read CSV file
    df = pd.read_csv(CSV_FILE)

    assert len(df) > 0

    # Connect to database using GitHub Actions environment variables
    connection = mysql.connector.connect(**DB_CONFIG)

    cursor = connection.cursor()

    # Check that transactions table exists
    cursor.execute("""
        SHOW TABLES LIKE 'transactions'
    """)

    table = cursor.fetchone()

    assert table is not None

    # Get database record count
    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
    """)

    database_count = cursor.fetchone()[0]

    # CSV and database should contain the same number of records
    assert len(df) == database_count

    cursor.close()
    connection.close()