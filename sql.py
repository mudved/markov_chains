import sqlite3

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
        print("Zapros completed OK")

    conn.commit()
    cursor.close()
    conn.close()

def input_db(cursor, table_name, string):
    sql = "SELECT id FROM {0} WHERE {0}='{1}'".format(table_name, string)
    cursor.execute(sql)
    string_id = cursor.fetchone()
    if string_id == None:
        sql = "INSERT OR IGNORE INTO {0} ({0}) VALUES ('{1}')".format(table_name, string) 
        cursor.execute(sql)
        string_id = cursor.lastrowid
    else:
        string_id = string_id[0]
    return string_id

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
    
    #tag_id = input_db_tag(cursor, 'tag_2444')
    tag_id = input_db(cursor, 'tag', 'proba_tag_2')
    #cat_id = input_db_category(cursor, 'cat_22')
    cat_id = input_db(cursor, 'category', 'proba_cat_2')
    #word_id= input_db_word(cursor, 'word_1')
    word_id = input_db(cursor, 'word', 'proba_word222_2')
    #window_id= input_db_window(cursor, 'window_1111xxxx')
    window_id = input_db(cursor, 'window', 'proba_window_2')

    window_word_id = input_window_word(cursor, 1, 1)
    print(window_word_id)
    conn.commit()
    
    cursor.close()
    conn.close()
