import sqlite3
import time
import random

def create_db_parser():

    name_db = 'parser_data\parserDB'
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

    CREATE TABLE url(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE);

    CREATE TABLE donor(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    donor TEXT NOT NULL UNIQUE);

    CREATE TABLE key(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL UNIQUE);

    CREATE TABLE video(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    video TEXT NOT NULL UNIQUE);

    CREATE TABLE actor(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    actor TEXT NOT NULL UNIQUE);

    CREATE TABLE content(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    url_id INTEGER NOT NULL REFERENCES url(id),
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

    CREATE TABLE content_donor(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    content_id INTEGER NOT NULL REFERENCES content(id),
    donor_id INTEGER NOT NULL REFERENCES donor(id));

    CREATE TABLE content_video(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    content_id INTEGER NOT NULL REFERENCES content(id),
    video_id INTEGER NOT NULL REFERENCES video(id));

    CREATE TABLE content_actor(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    content_id INTEGER NOT NULL REFERENCES content(id),
    actor_id INTEGER NOT NULL REFERENCES actor(id));

    CREATE TABLE content_category(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    content_id INTEGER NOT NULL REFERENCES content(id),
    category_id INTEGER NOT NULL REFERENCES category(id));

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

def input_db(conn, table_name, options:dict):
    '''Функция для добавления значения в таблицу БД. 
    table_name - имя таблицы для добавления записи,
    options - словарь входных значений в формате {'имя колонки таблицы':'значение'}'''

    cursor = conn.cursor()
    rows = options.keys()

    first = True
    for i in rows: 
        if first:
            string = "{0}='{1}'".format(i, options[i])
            string_rows = "'{}'".format(i)
            string_options = "'{}'".format(options[i])
            first = False
        else:
            string += " AND {0}='{1}'".format(i, options[i])
            string_rows += ", '{0}'".format(i)
            string_options += ", '{0}'".format(options[i])

    sql = "SELECT id FROM {0} WHERE {1}".format(table_name, string)

    while True:
        try:    
            cursor.execute(sql)
            string_id = cursor.fetchone()
            break
        except sqlite3.DatabaseError as err:
            print("input_db SELECT Error: ", err)
            time.sleep(random.randint(1,5))

    if string_id == None:
        sql = "INSERT OR IGNORE INTO {0} ({1}) VALUES ({2})".format(table_name, string_rows, string_options) 

        while True:
            try:
                cursor.execute(sql)
            except sqlite3.DatabaseError as err:
                print("input_db INSERT Error: ", err)
                time.sleep(random.randint(1,5))
            else:
                conn.commit()
                string_id = cursor.lastrowid
                break
    else:
        string_id = string_id[0]

    cursor.close()
    return string_id


if __name__ == '__main__':
    create_db_parser()
    conn = sqlite3.connect(r'parser_data\parserDB')
    options = {'tag':'tag_two'}
    id_tag = input_db(conn, 'tag', options)
    print(id_tag)
    
    options = {'key':'key'}
    id_key= input_db(conn, 'key', options)
    print(id_key)

    options = {'url':'url'}
    id_url= input_db(conn, 'url', options)
    print(id_url)
    
    options = {'image':'image'}
    id_image= input_db(conn, 'image', options)
    print(id_image)

    options = {'category':'category'}
    id_category= input_db(conn, 'category', options)
    print(id_category)

    options = {'donor':'donor'}
    id_donor= input_db(conn, 'donor', options)
    print(id_donor)

    options = {'video':'video'}
    id_video= input_db(conn, 'video', options)
    print(id_video)

    options = {'url_id':id_url, 'title':'First title', 'description':'desc-desc', 'h1':'zagolovok', 'content':'first content text'}
    id_content= input_db(conn, 'content', options)
    print(id_content)

    options = {'content_id':id_content, 'tag_id':id_tag}
    id_content_tag = input_db(conn, 'content_tag', options)
    print(id_content_tag)

    options = {'content_id':id_content, 'image_id':id_image}
    id_content_image= input_db(conn, 'content_image', options)
    print(id_content_image)

    options = {'content_id':id_content, 'key_id':id_key}
    id_content_key= input_db(conn, 'content_key', options)
    print(id_content_key)

    options = {'content_id':id_content, 'video_id':id_video}
    id_content_video= input_db(conn, 'content_video', options)
    print(id_content_video)

    options = {'content_id':id_content, 'category_id':id_category}
    id_content_category= input_db(conn, 'content_category', options)
    print(id_content_category)

    options = {'content_id':id_content, 'donor_id':id_donor}
    id_content_donor= input_db(conn, 'content_donor', options)
    print(id_content_donor)
    
    conn.close()
