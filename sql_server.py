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

        return True, "Connected successfully!"
    
    except psycopg2.OperationalError as e:
        return False, f"Connection failed: {e}"

def create_table():
    pass