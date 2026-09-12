import psycopg2
from psycopg2 import sql, OperationalError

# Connect to PostgreSQL Database
def connection(username, password, host):
    try:
        connection = psycopg2.connect(
            host=host,
            database="LastFrontier",
            user=username,
            password=password,
            port=5432
        )

        return True, connection

    except psycopg2.OperationalError as e:
        return False, f"Connection failed: {e}"

# Check if table already exists in DB
def find_table(db_connection, table_name, schema='public'):
    try:
        cursor = db_connection.cursor()

        query = sql.SQL("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = %s
                AND table_name = %s
            );
        """)

        cursor.execute(query, (schema, table_name))
        exists = cursor.fetchone()[0]
        cursor.close()

        return exists

    except Exception as e:
        print(f"Error checking table existence: {e}")
        return False

# Provides list of pre-detemined list of data types for JSON output 
def postgres_type(column_name, value):

    if column_name == "Time":
        return "TIMESTAMPTZ"

    elif isinstance(value, bool):
        return "BOOLEAN"

    elif isinstance(value, int):
        return "INTEGER"

    elif isinstance(value, float):
        return "DOUBLE PRECISION"

    elif isinstance(value, str):
        return "TEXT"

    else:
        return "TEXT"

# Create new table in DB
def create_table(db_connection, table_name, columns_dict):
    try:
        cursor = db_connection.cursor()
        columns = []

        for col_name, value in columns_dict.items():
            data_type = postgres_type(
                col_name,
                value
            )

            column = sql.SQL("{} {}").format(
                sql.Identifier(col_name),
                sql.SQL(data_type)
            )

            columns.append(column)

        create_table_sql = sql.SQL(
            "CREATE TABLE {} ({})"
        ).format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(columns)
        )

        cursor.execute(create_table_sql)
        db_connection.commit()
        cursor.close()

        return True, "Table created."

    except Exception as error:
        db_connection.rollback()
        return False, str(error)

# inserts weather data
def insert_data(db_connection, table_name, data_dict):
    try:
        cursor = db_connection.cursor()

        for column, value in data_dict.items():

            check_column = """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name = %s
                    AND column_name = %s
                );
            """

            cursor.execute(
                check_column,
                (table_name, column)
            )

            column_exists = cursor.fetchone()[0]

            if not column_exists:

                if isinstance(value, bool):
                    data_type = "BOOLEAN"
                elif isinstance(value, int):
                    data_type = "INTEGER"
                elif isinstance(value, float):
                    data_type = "DOUBLE PRECISION"
                elif column == "Time":
                    data_type = "TIMESTAMPTZ"
                else:
                    data_type = "TEXT"

                alter_table = sql.SQL(
                    "ALTER TABLE {} ADD COLUMN {} {}"
                ).format(
                    sql.Identifier(table_name),
                    sql.Identifier(column),
                    sql.SQL(data_type)
                )

                cursor.execute(alter_table)

        columns = [
            sql.Identifier(column)
            for column in data_dict.keys()
        ]

        values = list(data_dict.values())

        placeholders = sql.SQL(", ").join(
            sql.Placeholder()
            for _ in values
        )

        query = sql.SQL(
            "INSERT INTO {} ({}) VALUES ({})"
        ).format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(columns),
            placeholders
        )

        cursor.execute(query, values)

        db_connection.commit()
        cursor.close()

        return True, "Data inserted."

    except Exception as error:
        db_connection.rollback()
        return False, str(error)