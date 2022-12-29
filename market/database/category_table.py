from . import conn, cursor
def create_category_table():
    sql = """CREATE TABLE IF NOT EXISTS category (
        category_id INT PRIMARY KEY AUTO_INCREMENT,
        category_name VARCHAR(50) NOT NULL
    )"""
    cursor.execute(sql)
    conn.commit()

