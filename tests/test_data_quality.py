import mysql.connector
import pytest


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


def test_database_connection(db_connection):
    assert db_connection.is_connected()


def test_record_count(db_connection):
    cursor = db_connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    )

    count = cursor.fetchone()[0]

    cursor.close()

    assert count > 0


def test_null_transaction_ids(db_connection):
    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE transaction_id IS NULL
        """
    )

    null_count = cursor.fetchone()[0]

    cursor.close()

    assert null_count == 0


def test_duplicate_transaction_ids(db_connection):
    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM (
            SELECT transaction_id
            FROM transactions
            GROUP BY transaction_id
            HAVING COUNT(*) > 1
        ) AS duplicates
        """
    )

    duplicate_count = cursor.fetchone()[0]

    cursor.close()

    assert duplicate_count == 0


def test_negative_quantity(db_connection):
    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE quantity <= 0
        """
    )

    invalid_count = cursor.fetchone()[0]

    cursor.close()

    assert invalid_count == 0


def test_invalid_unit_price(db_connection):
    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE unit_price <= 0
        """
    )

    invalid_count = cursor.fetchone()[0]

    cursor.close()

    assert invalid_count == 0


def test_total_amount_calculation(db_connection):
    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE ABS(total_amount - (quantity * unit_price)) > 0.01
        """
    )

    invalid_count = cursor.fetchone()[0]

    cursor.close()

    assert invalid_count == 0