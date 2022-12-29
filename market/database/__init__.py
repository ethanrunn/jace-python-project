# create db connection
import mysql.connector as connector
from dotenv import dotenv_values

ENV = dotenv_values(".env")

# connect to mysql
try:
    conn = connector.connect(
        host=ENV.get("DB_HOST"),
        username=ENV.get("DB_USERNAME"),
        password=ENV.get("DB_PASSWORD"),
        database=ENV.get("DB_NAME")
    )

    # create a cursor
    cursor = conn.cursor(dictionary=True)

except Exception as e:
    print("Error connecting", e)


# # check if its connected
# if conn.is_connected():
#     print("DATABASE CONNECTED")
# else:
#     print("FAILED TO CONNECT TO DB")

# sql = "insert into student(name, course) values('Joshua Paul', 'Python SQL')"
# cursor.execute(sql)

# # commit the change
# conn.commit()

# if cursor.rowcount == 1:
#     print(f"{cursor.rowcount} record added to database")
