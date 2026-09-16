import psycopg2
import os

from psycopg2 import sql

def connection():
    try:
        user_host = os.getenv("DB_HOST")
        user_db_name = os.getenv("DB_NAME")
        user_name = os.getenv("DB_USER")
        user_password = os.getenv("DB_PASS")
        user_port = os.getenv("DB_PORT")

        connection = psycopg2.connect(
            host=user_host,
            database=user_db_name,
            user=user_name,
            password=user_password,
            port=user_port
        )

        return True, connection

    except psycopg2.OperationalError as error:
        return False, f"Connection failed: {error}"

def find_table(db_connection, table_name, schema="public"):
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

        cursor.execute(
            query,
            (schema, table_name)
        )

        exists = cursor.fetchone()[0]
        cursor.close()

        return exists

    except Exception as error:
        print(f"Error checking table existence: {error}")
        return False

def postgres_type(column_name, value):

    if column_name.lower() == "time_utc":
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

def create_table(
    db_connection,
    table_name,
    column_names,
    column_values
):
    try:
        cursor = db_connection.cursor()

        columns = []

        for column_name, value in zip(
            column_names,
            column_values
        ):

            data_type = postgres_type(
                column_name,
                value
            )

            column = sql.SQL("{} {}").format(
                sql.Identifier(column_name),
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

        return True, f"Table '{table_name}' has been created."

    except Exception as error:
        db_connection.rollback()
        return False, str(error)

def insert_data(db_connection, table_name, data_dict):
    try:
        cursor = db_connection.cursor()

        for column, value in data_dict.items():

            if isinstance(value, (dict, list, tuple, set)):
                return (
                    False,
                    f"Column '{column}' contains unsupported "
                    f"data type: {type(value).__name__}."
                )

            check_column = """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = %s
                    AND column_name = %s
                );
            """

            cursor.execute(
                check_column,
                (table_name, column)
            )

            column_exists = cursor.fetchone()[0]

            if not column_exists:

                data_type = postgres_type(
                    column,
                    value
                )

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

        return True

    except Exception as error:
        db_connection.rollback()
        return False, str(error)


def create_or_insert(db_connection, table_name, data_dict):
    table_exists = find_table(
        db_connection=db_connection,
        table_name=table_name
    )

    if table_exists is False:

        status, message = create_table(
            db_connection=db_connection,
            table_name=table_name,
            column_names=list(data_dict.keys()),
            column_values=list(data_dict.values())
        )

        if status is False:
            return False, message

        table_message = message

    else:

        table_message = (
            f"Table '{table_name}' exists. Inserting data to table.\n"
        )

    success, message = insert_data(
        db_connection=db_connection,
        table_name=table_name,
        data_dict=data_dict
    )

    if success is False:
        return False, message

    return True, table_message

def find_existing_row(db_connection, table_name, rows_dict):
    try:
        cursor = db_connection.cursor()
        rows_dict = {
            key: value
            for key, value in rows_dict.items()
            if key != "time_utc"
        }
  
        where_clause = sql.SQL(" AND ").join(
            sql.Composed([
                sql.Identifier(col),
                sql.SQL(" = "),
                sql.Placeholder()
            ])
            for col in rows_dict.keys()
        )

        query = sql.SQL("SELECT * FROM {table} WHERE {conditions}").format(
            table=sql.Identifier(table_name),
            conditions=where_clause
        )

        values = tuple(rows_dict.values())

        cursor.execute(query, values)

        rows = cursor.fetchall()
        return True, len(rows)
    
    except Exception as error:
        db_connection.rollback()
        return False, str(error)
