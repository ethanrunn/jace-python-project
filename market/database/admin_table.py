from . import conn, cursor

def create_admin_table():
    sql = """CREATE TABLE IF NOT EXISTS admin(
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(255) 
    )"""
    cursor.execute(sql)
    conn.commit()
    print("TABLE CREATED!!")