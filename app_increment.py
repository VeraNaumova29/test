from lesson_7 import *
from increment import *

config = get_config()
connection = get_connection(config)
cursor = connection.cursor()

create_and_set_schema(cursor, connection, "auto")
remove_tmp_tables(cursor, connection)
create_hist_auto(cursor, connection)
create_v_auto(cursor, connection)

csv_to_sql("store/data_1.csv", "tmp_auto", "auto", config)
create_new_rows(cursor, connection)
create_deleted_rows(cursor, connection)
create_updated_rows(cursor, connection)
update_hist_auto(cursor, connection)

close(connection, cursor)