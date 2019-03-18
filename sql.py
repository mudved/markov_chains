import sqlite3

conn = sqlite3.connect("testdatabase.db")
cursor = conn.cursor()

sql = """
CREATE TABLE tag(
id INTEGER PRIMARY KEY AUTOINCREMENT,
tag TEXT);

CREATE TABLE category(
id INTEGER PRIMARY KEY AUTOINCREMENT,
category TEXT);

CREATE TABLE word(
id INTEGER PRIMARY KEY AUTOINCREMENT,
word TEXT);

CREATE TABLE window_3(
id INTEGER PRIMARY KEY AUTOINCREMENT,
word_1 TEXT,
word_2 TEXT,
word_3 TEXT);

CREATE TABLE window_3_word(
id INTEGER PRIMARY KEY AUTOINCREMENT,
word_id INTEGER,
window_id INTEGER,
count INTEGER);

CREATE TABLE w3w_tag(
id INTEGER PRIMARY KEY AUTOINCREMENT,
w3w_id INTEGER,
tag_id INTEGER);

CREATE TABLE w3w_category(
id INTEGER PRIMARY KEY AUTOINCREMENT,
w3w_id INTEGER,
category_id);"""

#cursor.execute("""CREATE TABLE WINDOW_3
#        (ID integer, WORD_1 text, WORD_2 text, WORD_3 text)""")

try:
    cursor.executescript(sql)
except sqlite.DatabaseError as err:
    print("Ошибка: ", err)
else:
    print("Запрос выполнен успешно")

conn.commit()
cursor.close()
conn.close()
