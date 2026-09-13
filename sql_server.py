import psycopg2
from psycopg2 import sql
from colorama import Fore, Style

required_tables = ["weather", "air_pollution"]


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


def create_table(db_connection, table_name, data_dict):
    try:
        cursor = db_connection.cursor()
        columns = []

        for column_name, value in data_dict.items():

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

        return True, f"Data inserted into '{table_name}'."

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
            data_dict=data_dict
        )

        if status is False:
            return False, message

        print(
            Fore.LIGHTGREEN_EX
            + message
            + Style.RESET_ALL
        )

    return insert_data(
        db_connection=db_connection,
        table_name=table_name,
        data_dict=data_dict
    )
