import psycopg2

# Establish connection with sql server
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

def find_table():
    pass

def create_table(db_connection, table_name, columns_dict):
    try:
        cursor = db_connection.cursor()

        columns_sql = ", ".join(
            f'"{col_name}" {data_type}'
            for col_name, data_type in columns_dict.items()
        )

        create_table_sql = f'CREATE TABLE "{table_name}" ({columns_sql});'

        cursor.execute(create_table_sql)
        db_connection.commit()
        cursor.close()

        return True, "Table created."

    except Exception as error:
        db_connection.rollback()
        return False, str(error)
