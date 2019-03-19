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
    tag TEXT NOT NULL UNIQUE);

    CREATE TABLE category(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL UNIQUE);

    CREATE TABLE word(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL UNIQUE);

    CREATE TABLE window_word(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL REFERENCES word(id),
    window_id INTEGER NOT NULL REFERENCES window(id),
    count INTEGER);

    CREATE TABLE ww_tag(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    ww_id INTEGER NOT NULL REFERENCES window_word(id),
    tag_id INTEGER NOT NULL REFERENCES tag(id));

    CREATE TABLE ww_category(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    ww_id INTEGER NOT NULL REFERENCES window_word(id),
    category_id INTEGER NOT NULL REFERENCES category(id));
      
    CREATE TABLE window(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    window TEXT NOT NULL UNIQUE);"""
     
    try:
        cursor.executescript(sql)
    except sqlite3.DatabaseError as err:
        print("Ошибка: ", err)
    else:
        print("Запрос выполнен успешно")

    conn.commit()
    cursor.close()
    conn.close()

def input_db_tag(cursor, tag):
    sql = "SELECT id FROM tag WHERE tag='{}'".format(tag)
    cursor.execute(sql)
    tag_id = cursor.fetchone()
    if tag_id == None:
        sql = "INSERT OR IGNORE INTO tag (tag) VALUES ('{}')".format(tag) 
        cursor.execute(sql)
        tag_id = cursor.lastrowid
    else:
        tag_id = tag_id[0]
    return tag_id

def input_db_category(cursor, category):
    sql = "SELECT id FROM category WHERE category='{}'".format(category)
    cursor.execute(sql)
    category_id = cursor.fetchone()
    if category_id == None:
        sql = "INSERT OR IGNORE INTO category (category) VALUES ('{}')".format(category) 
        cursor.execute(sql)
        category_id = cursor.lastrowid
    else:
        category_id = category_id[0]
    return category_id

def input_db_word(cursor, word):
    sql = "SELECT id FROM word WHERE word='{}'".format(word)
    cursor.execute(sql)
    word_id = cursor.fetchone()
    if word_id == None:
        sql = "INSERT OR IGNORE INTO word (word) VALUES ('{}')".format(word) 
        cursor.execute(sql)
        word_id = cursor.lastrowid
    else:
        word_id = word_id[0]
    return word_id

def input_db_window(cursor, window):
    sql = "SELECT id FROM window WHERE window='{}'".format(window)
    cursor.execute(sql)
    window_id = cursor.fetchone()
    if window_id == None:
        sql = "INSERT OR IGNORE INTO window (window) VALUES ('{}')".format(window) 
        cursor.execute(sql)
        window_id = cursor.lastrowid
    else:
        window_id = window_id[0]
    return window_id

def input_window_word(cursor, window_id, word_id):
    sql = "SELECT id, count FROM window_word WHERE window_id='{0}' AND word_id='{1}'".format(window_id, word_id)
    cursor.execute(sql)
    window_word_id = cursor.fetchall()
    if window_word_id == []:
        sql = "INSERT OR IGNORE INTO window_word (window_id, word_id, count) VALUES ('{0}', '{1}', '1')".format(window_id, word_id) 
        cursor.execute(sql)
        window_word_id = cursor.lastrowid
    else:
        window_word_id = window_word_id[0][0]
    return window_word_id


if __name__ == '__main__':
    #create_db()
    #create_db(1)
    #create_db(2)

    conn = sqlite3.connect('markovdb_order3')
    cursor = conn.cursor()
    
    tag_id = input_db_tag(cursor, 'tag_2444')
    cat_id = input_db_category(cursor, 'cat_22')
    word_id= input_db_word(cursor, 'word_1')
    window_id= input_db_window(cursor, 'window_1111xxxx')
    window_word_id = input_window_word(cursor, 1, 1)
    print(window_word_id)
    conn.commit()
    
    cursor.close()
    conn.close()
