import mysql.connector
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


# Connect to MySQL
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


# Insert / Update / Delete
def execute_query(query, values=None):

    connection = get_connection()
    cursor = connection.cursor()

    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)

    connection.commit()

    cursor.close()
    connection.close()


# Get one record
def fetch_one(query, values=None):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


# Get multiple records
def fetch_all(query, values=None):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result
# if __name__ == "__main__":

#     connection = get_connection()

#     if connection.is_connected():
#         print("MySQL Connected Successfully")

#     connection.close()
