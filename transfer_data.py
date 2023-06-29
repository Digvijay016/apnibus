import sqlite3

source_conn = sqlite3.connect('dummy_3.sqlite3')
target_conn = sqlite3.connect('dummy.sqlite3')

source_cursor = source_conn.cursor()
target_cursor = target_conn.cursor()

# Create the bus_busroute table in the target database
target_cursor.execute('''
    CREATE TABLE IF NOT EXISTS bus_busroute (
        id TEXT PRIMARY KEY,
        from_town TEXT NOT NULL,
        to_town TEXT NOT NULL,
        start_time TEXT NOT NULL,
        arrival_time TEXT NOT NULL,
        route_ids TEXT,
        bus_id TEXT,
        via TEXT,
        history TEXT
    )
''')

# source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tables = source_cursor.fetchall()

# for table in tables:
#     # table_name = table[0]
#     table_name = 'bus_busroute'
#     source_cursor.execute(f"SELECT * FROM {table_name};")
#     rows = source_cursor.fetchall()
#     for row in rows:
#         # Skip the columns 'created_on', 'updated_on', and 'is_deleted'
#         row = row[:6] + row[9:]
#         target_cursor.execute(f"INSERT INTO {table_name} VALUES ({','.join(['?'] * len(row))});", row)

target_conn.commit()
source_conn.close()
target_conn.close()


# import sqlite3

# source_conn = sqlite3.connect('dummy.sqlite3')
# target_conn = sqlite3.connect('dummy_3.sqlite3')

# source_cursor = source_conn.cursor()
# target_cursor = target_conn.cursor()

# source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tables = source_cursor.fetchall()

# for table in tables:
#     # table_name = table[0]
#     table_name = 'bus_busroute'
#     if table_name in ('django_migrations', 'django_content_type', 'auth_permission'):
#         continue  # Skip the django_migrations table

#     source_cursor.execute(f"PRAGMA table_info({table_name});")
#     columns = source_cursor.fetchall()
#     column_names = [column[1] for column in columns]

#     source_cursor.execute(f"SELECT * FROM {table_name};")
#     rows = source_cursor.fetchall()

#     for row in rows:
#         # Remove the unwanted columns from the row
#         filtered_row = [value for idx, value in enumerate(row) if column_names[idx] not in [
#             'created_on', 'updated_on', 'is_deleted']]

#         target_cursor.execute(
#             f"INSERT INTO {table_name} VALUES ({','.join(['?'] * len(filtered_row))});")

#     # source_cursor.execute(f"SELECT * FROM {table_name};")
#     # rows = source_cursor.fetchall()
#     # for row in rows:
#     #     target_cursor.execute(
#     #         f"INSERT INTO {table_name} VALUES ({','.join(['?'] * len(row))});", row)

# target_conn.commit()
# source_conn.close()
# target_conn.close()
