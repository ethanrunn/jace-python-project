from . import conn, cursor
def create_product_table():
    sql = """CREATE TABLE IF NOT EXISTS product (
        product_id VARCHAR(50) PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        category VARCHAR(40) NOT NULL,
        price VARCHAR(100) NOT NULL,
        quantity INT NOT NULL,
        image VARCHAR(255) NOT NULL,
        date DATETIME DEFAULT CURRENT_TIMESTAMP
    )"""
    cursor.execute(sql)
    conn.commit()
