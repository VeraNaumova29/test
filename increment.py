"""
create_new_rows
    создает таблицу с новыми записями
create_updated_rows
    создает таблицу с измененными записями
create_deleted_rows
    создает таблицу с удаленными записями
remove_tmp_tables
    удаляет уже имеющиеся таблицы
"""
def create_new_rows(cursor, connection):
    cursor.execute("""
        CREATE TABLE tmp_new_rows as
            select
                t1.model,
                t1.transmission,
                t1.body_type,
                t1.drive_type,
                t1.color,
                t1.production_year,
                t1.auto_key,
                t1.engine_capacity,
                t1.horsepower,
                t1.engine_type,
                t1.price,
                t1.milage  
            from auto_key t1
            left join hist_auto t2
            on t1.auto_key = t2.auto.key
            where t2.auto_key is null
    """)
    connection.commit()

def create_deleted_rows(cursor, connection):
    cursor.execute("""
        CREATE TABLE tmp_deleted_rows as
            select
                t1.model,
                t1.transmission,
                t1.body_type,
                t1.drive_type,
                t1.color,
                t1.production_year,
                t1.auto_key,
                t1.engine_capacity,
                t1.horsepower,
                t1.engine_type,
                t1.price,
                t1.milage  
            from hist_auto t1
            left join tmp_auto t2
            on t1.auto_key = t2.auto.key
            where t2.auto_key is null
    """)
    connection.commit()

def create_updated_rows(cursor, connection):
    cursor.execute("""
        CREATE TABLE tmp_updated_rows as
            select
                t2.model,
                t2.transmission,
                t2.body_type,
                t2.drive_type,
                t2.color,
                t2.production_year,
                t2.auto_key,
                t2.engine_capacity,
                t2.horsepower,
                t2.engine_type,
                t2.price,
                t2.milage  
            from hist_auto t1
            inner join tmp_auto t2
            on t1.auto_key = t2.auto.key
            where t1.model <> t2.model
                or t1.transmission <> t2.transmission
                or t1.body_type <> t2.body_type
                or t1.drive_type <> t2.drive_type
                or t1.color <> t2.color
                or t1.production_year <> t2.production_year
                or t1.engine_capacity <> t2.engine_capacity
                or t1.horsepower <> t2.horsepower
                or t1.engine_type <> t2.engine_type
                or t1.price <> t2.price
                or t1.milage <> t2.milage
    """)
    connection.commit()

def remove_tmp_tables(cursor, connection):

    cursor.execute("""
        SELECT
            table_name
        from information_schema.tables
        where table_schema = 'auto'
        and table_name like 'tmp_%'
    """)

    for table in cursor.fetchall():
        cursor.execute(f'DROP TABLE if exists {table[0]}')
    
    connection.commit()

    cursor.execute("DROP TABLE if exists tmp_auto")
    cursor.execute("DROP TABLE if exists tmp_new_rows")
    cursor.execute("DROP TABLE if exists tmp_deleted_rows")
    cursor.execute("DROP TABLE if exists tmp_updated_rows")

    connection.commit()

def update_hist_auto(cursor, connection):
    cursor.execute("""
        INSERT INTO hist_auto (
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
            )
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
            from tmp_new_rows
    """)

    # 1) изменить у записей с тем же auto_key end_dttm на текущий момент времени минус 1
    # 2) добавляем измененные записи

    cursor.execute("""
        UPDATE hist_auto
        set end_dttm = now() - interval '1 second'
        where auto_key in (
            select
                auto_key
            from tmp_updated_rows
        )
        and `end_dttm = '2999-12-31 23:59:59'`
    """)

    cursor.execute("""
        INSERT INTO hist_auto (
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
        )
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
        from tmp_updated_rows                   
    """)

    # 3) указать для удаленных записей end_dttm
    # 4) добавить новую запись про удаленные данные с deleted_flg = 1

    cursor.execute("""
            INSERT INTO hist_auto (
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
                milage,
                deleted_flg
            )
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
                milage,
                1
            from tmp_deleted_rows                   
        """)

    connection.commit()


