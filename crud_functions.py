import sqlite3

def initiate_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_sample_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    sample_products = [
        ("Product1", "Описание 1", 100),
        ("Product2", "Описание 2", 200),
        ("Product3", "Описание 3", 300),
        ("Product4", "Описание 4", 400),
    ]

    cursor.executemany('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', sample_products)
    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    conn.close()
    return products

def clear_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Products')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initiate_db()
    clear_products()  
    add_sample_products()
    print("Таблица Products успешно инициализирована и заполнена тестовыми данными:")
    print(get_all_products())




