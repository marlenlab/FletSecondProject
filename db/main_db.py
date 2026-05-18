import sqlite3
from config import path_db
from db import queries

def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.create_tasks_table)
    print('БД Подключена!')
    conn.commit()
    conn.close