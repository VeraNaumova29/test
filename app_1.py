import psycopg2

connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="12345678",
        host="localhost",
        port="5432"
    )

cursor = connection.cursor()

def read(source):
    cursor.execute(f"select * from {source};")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def create_products():
    cursor.execute(""" 
        CREATE TABLE sbx.products (
            products_id SERIAL PRIMARY KEY,
            title VARCHAR(50),
            price integer,
            discount integer default 0 ,
            count integer
        );
    """)
    connection.commit()

def add_products(title, price, discount, count):
    cursor.execute(""" 
        INSERT INTO sbx.products (
            title,
            price,
            discount,
            count
        )values(%s, %s, %s, %s)
    """, [title, price, discount, count])
    connection.commit() 

def add_unique_product(title):
    cursor.execute('''
        select 
            title,
            round(price - (price/100)*discount, 2)
        from sbx.products
        where title = %s
    ''', [title])

    result = cursor.fetchone()
    
    if result == 0:
        print(f"Пордукта {title} в базе нет")
    return result
    
    #add_products(title, price, discount, count)

def sale(title, count):
    cursor.execute('''
        UPDATE sbx.products 
        set count = count - %s
        where title = %s
    ''', [count, title])  
    connection.commit() 



#print(add_unique_product('more'))
#create_products()
#add_products('title', 23.45, 20, 2)

sale('more', 2)
read('sbx.products')








cursor.close()
connection.close()