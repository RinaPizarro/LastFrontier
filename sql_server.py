import psycopg2
from psycopg2.extras import Json

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

# Detect data types prior to creating table
def get_data_types(conn, data):
    cur = None

    try:
        cur = conn.cursor()

        # Send dictionary as JSONB and detect type
        cur.execute("SELECT pg_typeof(%s)", (Json(data),))
        pg_type = cur.fetchone()[0]
        print(f"PostgreSQL detected type: {pg_type}")

        # Optional: Get OID and type name
        cur.execute("SELECT oid, typname FROM pg_type WHERE typname = %s", (pg_type,))
        print("OID and type name:", cur.fetchone())

    except psycopg2.Error as e:
        print("Database error:", e)

    finally:
        # Close cursor if it was created
        if cur is not None:
            cur.close()
        # Close connection if it was created
        if conn is not None:
            conn.close()

# Create table in SQL server
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

    except:
        return False, "Cannot create table"
