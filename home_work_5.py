import psycopg2
import json

table_name = "sbx.client"

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

#считать и вернуть содержимое таблицы
def read(source):
    cursor.execute(f"select * from {source};")
    rows = cursor.fetchall()
    return rows

def create_client(m_table_name):
    cursor.execute(f"""
        CREATE TABLE {m_table_name} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            last_name VARCHAR(50),
            age integer
        );
    """)
    connection.commit()

try:
    create_client(table_name)
except Exception as e:
    print(f'Таблица "{table_name}" уже существует: {e}')
    connection.commit()


def add_client(name, last_name, age):
    cursor.execute("select * from sbx.client where name = %s and last_name = %s;", [name, last_name])
    rows = cursor.fetchall()
    
    if not rows:
        print("ADD")
        cursor.execute(""" 
            INSERT INTO sbx.client (
                name,
                last_name,
                age
            )values(%s, %s, %s)
        """, [name, last_name, age])
        connection.commit() 


def get_json_file(path="hw_5.json"):
    with open(path, "r", encoding='utf-8') as f:
        peoples_list = json.load(f)
    for piple in peoples_list:
        add_client(piple['name'], piple['last_name'], piple['age'])


def avg_age(d):
    sum_age = 0
    for s in d:
        sum_age += s['age']
    return sum_age/len(d)

print(avg_age(peoples_list))


cursor.close()
connection.close()
