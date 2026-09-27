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


def test_csv_to_mysql_integration():

    df = pd.read_csv(CSV_FILE)

    assert len(df) > 0

    connection = mysql.connector.connect(**DB_CONFIG)

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    )

    database_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    assert len(df) == database_count