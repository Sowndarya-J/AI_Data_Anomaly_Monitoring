import mysql.connector


def get_connection():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="#Sownd@1710#",
        database="anomaly_monitoring"
    )

    return connection


if __name__ == "__main__":

    connection = get_connection()

    if connection.is_connected():
        print("MySQL connection successful!")

    connection.close()

    print("MySQL connection closed.")