import psycopg2
import json
import pandas as pd
from sqlalchemy import create_engine

table_name = "sbx.users"

try:
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="12345678",
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()

except Exception as e:
    print(f"Ошибка: {e}")

#подключение к схеме базы
cursor.execute("SET search_path to sbx;")

#создание таблицы
def create_users(m_table_name):
    try:
        cursor.execute(f"""
            CREATE TABLE {m_table_name} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                last_name VARCHAR(50),
                age integer,
                salary integer,
                start_dttm TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_dttm TIMESTAMP DEFAULT '2999-12-31 23:59:59',
                deleted NUMERIC DEFAULT 0
            );
        """)
        connection.commit()
    except Exception as e:
        print(f'Таблица "{m_table_name}" уже существует: {e}')
        connection.rollback()
        cursor.execute(f"DROP TABLE if exists {m_table_name}")
        connection.commit()
        print(f'Поэтому таблицу "{m_table_name}" мы удалим и создадим')
        create_users(m_table_name)
        connection.commit()



def add_user(name, last_name, age, salary):
    cursor.execute("select id from sbx.users where name = %s and last_name = %s and now() between start_dttm and end_dttm;", [name, last_name])
    rows = cursor.fetchall()

    if rows:
        cursor.execute("""
        UPDATE sbx.users
        set end_dttm = now() - interval '1 second'
        where id = %s
        """, [rows[0][0]])
        connection.commit()

    print("Добавление нового пользователя")
    cursor.execute(""" 
        INSERT INTO sbx.users (
            name,
            last_name,
            age,
            salary
        )values(%s, %s, %s, %s)
    """, [name, last_name, age, salary])
    connection.commit()

def delete_user(name, last_name):
    cursor.execute("update sbx.users set deleted = 1 where name = %s and last_name = %s;", [name, last_name])
    connection.commit()

 
def sql_to_csv(path, time='now()'):
    connection = create_engine("postgresql://postgres:12345678@localhost:5432/postgres")
    data = pd.read_sql_query(f'select * from sbx.users where {time} between start_dttm and end_dttm;', con=connection)
    data.to_csv(path)
    
create_users(table_name)
add_user('vera', 'naumova', 32, 250000)
add_user('lera', 'zayceva', 40, 100000)
add_user('vera', 'naumova', 33, 300000)
add_user('maxim', 'naumov', 43, 400000)

delete_user('maxim', 'naumov')

sql_to_csv('file.csv')

cursor.close()
connection.close()