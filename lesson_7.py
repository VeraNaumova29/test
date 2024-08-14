import json
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

def get_config(path="db_config.json"):
    with open(path, "r") as f:
        config = json.load(f)
        return config
    
def get_connection(config):
    connection = psycopg2.connect(**config)
    return connection

def close(connection=None, cursor=None):
    if cursor:
        cursor.close()
    
    if connection:
        connection.close()

def csv_to_sql(path, table, schema, c):
    connect_str = f"postgresql://{c['user']}:{c['password']}@{c['host']}:{c['port']}/{c['dbname']}"
    connection = create_engine(connect_str)
    df = pd.read_csv(path)
    df.to_sql(name=table, con=connection, schema=schema, if_exists="replace", index=False)

def create_hist_auto(cursor, connection):
    cursor.execute("""
        CREATE TABLE if not exists hist_auto(
            id serial primary key,
            model,
            transmission,
            body_type,
            drive_type,
            color,
            production_year,
            auto_key,
            engine_capacity,
            horsepower,
            engine_type,
            price,
            milage)
    """)
    connection.commit()

def create_v_auto(cursor, connection):
    cursor.execute("""
        DROP VIEW v_auto as
            select
                model,
                transmission,
                body_type,
                drive_type,
                color,
                production_year,
                auto_key,
                engine_capacity,
                horsepower,
                engine_type,
                price,
                milage                   
            from hist_auto
            where end_dttm = '2999-12-31 23:59:59'
                and deleted_flg = 0
    """)
    connection.commit()

def create_and_set_schema(cursor, connection, schema_name):
    cursor.execute(f"create schema if not exist {schema_name};")
    cursor.execute(f"set search_path to {schema_name};")
    connection.commit()

config = get_config()
connection = get_connection(config)
cursor = connection.cursor()
cursor.execute("create schema if not exists auto")
cursor.execute("set search_path to auto")
connection.commit()

csv_to_sql("test.csv", "tmp_table", "auto", config)
create_hist_auto(cursor, connection)

close(connection, cursor)


