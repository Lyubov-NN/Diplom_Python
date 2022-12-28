import psycopg2

from path_base import *

conn = psycopg2.connect(database=database, user=user, password=password)


conn.autocommit = True


# Функция, создающая структуру БД (таблицу)
def create_table():
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_choice (
            id SERIAL PRIMARY KEY,
            users INTEGER NOT NULL,
            choice INTEGER NOT NULL
        );
                """)

# Функция, позволяющая добавить нового пользователя и его выбор
def add_client(user, choice):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO user_choice(users, choice) VALUES(%s, %s) RETURNING id, users, choice;
                    """, (user, choice))
        # print(cur.fetchone())


# Функция, позволяющая найти клиента и его выбор
def find_client(user, choice):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT 1
        FROM user_choice
        WHERE users = %s and choice = %s;
                    """, (user, choice))
        return cur.fetchall()


# print(find_client(6186222, 339235457))