import psycopg2

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

cursor.execute("set search_path to sbx;")

def read(source):
    cursor.execute(f"select * from {source};")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def create_employees():
    cursor.execute(""" 
        CREATE TABLE if not exists employees (
            employee_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100) UNIQUE NOT NULL,
            hire_date DATE NOT NULL,
            salary NUMERIC(10, 2) NOT NULL
        );
    """)
    connection.commit()

def add_employees(data_list):
    cursor.execute(""" 
        INSERT INTO employees (
            first_name,
            last_name,
            email,
            hire_date,
            salary
        )values(%s, %s, %s, %s, %s)
    """, data_list)
    connection.commit()    


create_employees()
add_employees(['John', 'Doe', 'john.doe@example.com', '2023-07-18', 60000.00])
read('employees')

cursor.close()
connection.close()
