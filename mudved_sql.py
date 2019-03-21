import sqlite3

def create_db_ozu(order=3):

    name_db = ':memory:'
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
        print("Error: ", err)
    else:
        print("DB is created")
        conn.commit()

    return conn

def create_db(order=3):

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
        print("Error: ", err)
    else:
        print("DB is created")
        conn.commit()

    cursor.close()
    conn.close()

def create_db_parser():

    name_db = 'parserDB'
    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()

    sql = """
    CREATE TABLE tag(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    tag TEXT NOT NULL UNIQUE);

    CREATE TABLE category(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL UNIQUE);

    CREATE TABLE image(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    image TEXT NOT NULL UNIQUE);

    CREATE TABLE donor(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    donor TEXT NOT NULL UNIQUE);

    CREATE TABLE key(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL UNIQUE);

    CREATE TABLE content(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    cat_id INTEGER NOT NULL REFERENCES category(id),
    donor_id INTEGER NOT NULL REFERENCES donor(id),
    title TEXT NOT NULL,
    description TEXT,
    h1 TEXT,
    content TEXT);

    CREATE TABLE content_tag(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    content_id INTEGER NOT NULL REFERENCES content(id),
    tag_id INTEGER NOT NULL REFERENCES tag(id));

    CREATE TABLE content_image(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    content_id INTEGER NOT NULL REFERENCES content(id),
    image_id INTEGER NOT NULL REFERENCES image(id));

    CREATE TABLE content_key(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    content_id INTEGER NOT NULL REFERENCES content(id),
    key_id INTEGER NOT NULL REFERENCES key(id));"""
     
    try:
        cursor.executescript(sql)
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        print("DB 'parserDB' is created")
        conn.commit()

    cursor.close()
    conn.close()

def input_db(conn, table_name, string):
    '''Функция для добавления значения в таблицу. Имя поля должно быть = имя таблицы и быть 
    единственным полем кроме поля ID'''

    cursor = conn.cursor()
    sql = "SELECT id FROM {0} WHERE {0}='{1}'".format(table_name, string)

    try:    
        cursor.execute(sql)
        string_id = cursor.fetchone()
    except sqlite3.DatabaseError as err:
        print("input_db Error: ", err)

    if string_id == None:
        sql = "INSERT OR IGNORE INTO {0} ({0}) VALUES ('{1}')".format(table_name, string) 

        try:
            cursor.execute(sql)
        except sqlite3.DatabaseError as err:
            print("input_db write Error: ", err)
        else:
            conn.commit()
            string_id = cursor.lastrowid
    else:
        string_id = string_id[0]

    cursor.close()
    return string_id

def input_window_word(conn, window_id, word_id):
    cursor = conn.cursor()
    sql = "SELECT id, count FROM window_word WHERE window_id='{0}' AND word_id='{1}'".format(window_id, word_id)

    try:
        cursor.execute(sql)
        window_word_id = cursor.fetchall()
    except sqlite3.DatabaseError as err:
        print("input_window_word Error: ", err)

    if window_word_id == []:
        sql = "INSERT OR IGNORE INTO window_word (window_id, word_id, count) VALUES ('{0}', '{1}', '1')".format(window_id, word_id) 

        try:
            cursor.execute(sql)
        except sqlite3.DatabaseError as err:
            print("input_window_word write Error: ", err)
        else:
            conn.commit()
            window_word_id = cursor.lastrowid
    else:
        window_word_count = window_word_id[0][1] + 1
        window_word_id = window_word_id[0][0]
        sql = "UPDATE window_word SET count = {0} WHERE id = {1}".format(window_word_count, window_word_id)

        try:
            cursor.execute(sql)
        except sqlite3.DatabaseError as err:
            print("input_window_word update Error: ", err)
        else:
            conn.commit()

    cursor.close()
    return window_word_id


if __name__ == '__main__':
    #create_db()
    #create_db(1)
    #create_db(2)

    conn = sqlite3.connect('markovdb_order3')
    
    tag_id = input_db(conn, 'tag', 'proba_tag_55')
    cat_id = input_db(conn, 'category', 'proba_cat_55')
    word_id = input_db(conn, 'word', 'proba_word_55')
    window_id = input_db(conn, 'window', 'proba_window_55')

    window_word_id = input_window_word(conn, window_id, word_id)
    
    conn.close()
