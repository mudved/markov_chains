import sqlite3

def create_db(order=3):
    """Создаёт базу данных для хранения модели цепи Маркова
    order - порядок цепи"""

    name_db = 'markovdb_order'+str(order)
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    sql = """
    CREATE TABLE tag(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    tag TEXT);

    CREATE TABLE category(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    category TEXT);

    CREATE TABLE word(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    word TEXT);


    CREATE TABLE window_word(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL REFERENCES word(id),
    window_id INTEGER NOT NULL REFERENCES window(id),
    count INTEGER);

    CREATE TABLE ww_tag(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    ww_id INTEGER,
    tag_id INTEGER);

    CREATE TABLE ww_category(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    ww_id INTEGER,
    category_id);
      
    CREATE TABLE window(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"""
     
    if order == 1:
        sql += """
                word_1 TEXT);
                """
    elif order == 2:
        sql += """
                word_1 TEXT,
                word_2 TEXT);
                """
    elif order == 3:
        sql += """
                word_1 TEXT,
                word_2 TEXT,
                word_3 TEXT);
                """
    elif order == 4:
        sql += """
                word_1 TEXT,
                word_2 TEXT,
                word_3 TEXT,
                word_4 TEXT);
                """

    try:
        cursor.executescript(sql)
    except sqlite3.DatabaseError as err:
        print("Ошибка: ", err)
    else:
        print("Запрос выполнен успешно")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    create_db()
    create_db(1)
    create_db(2)
