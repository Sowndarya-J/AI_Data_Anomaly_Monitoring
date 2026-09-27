import pandas as pd

from database.db_connection import get_connection


CSV_FILE = "data/processed/ecommerce_transactions_clean.csv"


def create_table(connection):
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id VARCHAR(50) PRIMARY KEY,
        date DATETIME,
        customer_id VARCHAR(50),
        product_id VARCHAR(50),
        quantity INT,
        unit_price DECIMAL(10, 2),
        payment_method VARCHAR(50),
        total_amount DECIMAL(15, 2)
    )
    """

    cursor.execute(create_table_query)
    connection.commit()

    cursor.close()

    print("Transactions table created successfully!")


def load_data(connection, df):
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO transactions
    (
        transaction_id,
        date,
        customer_id,
        product_id,
        quantity,
        unit_price,
        payment_method,
        total_amount
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    records = []

    for _, row in df.iterrows():
        records.append(
            (
                row["transaction_id"],
                pd.to_datetime(row["date"]).to_pydatetime(),
                row["customer_id"],
                row["product_id"],
                int(row["quantity"]),
                float(row["unit_price"]),
                row["payment_method"],
                float(row["total_amount"])
            )
        )

    if records:
        cursor.executemany(insert_query, records)
        connection.commit()

        print(f"{cursor.rowcount} records inserted successfully!")
    else:
        print("No records found to insert.")

    cursor.close()


def main():
    print("Loading processed CSV...")

    df = pd.read_csv(CSV_FILE)

    print(f"CSV records found: {len(df)}")

    connection = get_connection()

    try:
        create_table(connection)

        load_data(connection, df)

    except Exception as error:
        connection.rollback()

        print("Error while loading data:")
        print(error)

        raise

    finally:
        connection.close()

        print("MySQL connection closed.")


if __name__ == "__main__":
    main()