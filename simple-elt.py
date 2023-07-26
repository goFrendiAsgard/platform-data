import psycopg2
from clickhouse_driver import Client

def extract_load():
    # PostgreSQL connection configuration
    postgres_host = 'localhost'
    postgres_port = '5432'
    postgres_db = 'mydb'
    postgres_user = 'postgres'
    postgres_password = 'admin'

    # ClickHouse connection configuration
    clickhouse_host = 'localhost'
    clickhouse_port = '9000'
    clickhouse_db = 'mydb'
    clickhouse_user = 'clickhouse'
    clickhouse_password = 'admin'

    # Connect to PostgreSQL and ClickHouse
    postgres_conn = psycopg2.connect(
        host=postgres_host,
        port=postgres_port,
        database=postgres_db,
        user=postgres_user,
        password=postgres_password
    )

    clickhouse_conn = Client(
        host=clickhouse_host,
        port=clickhouse_port,
        database=clickhouse_db,
        user=clickhouse_user,
        password=clickhouse_password
    )

    # Read data from PostgreSQL
    postgres_cursor = postgres_conn.cursor()
    postgres_cursor.execute('SELECT id, vote_time, voter, candidate FROM voting')
    pg_rows = postgres_cursor.fetchall()
    rows = []
    for row in pg_rows:
        row = list(row)
        row[1] = str(row[1]).split('.')[0]
        rows.append(row)


    # print(clickhouse_conn.execute('SHOW TABLES'))
    # Insert data into ClickHouse
    clickhouse_query = 'INSERT INTO voting_copy (id, vote_time, voter, candidate) VALUES'
    clickhouse_data = ','.join(f"({row[0]}, '{row[1]}', '{row[2]}', '{row[3]}')" for row in rows)
    print(clickhouse_query + clickhouse_data + ';')
    clickhouse_conn.execute(clickhouse_query + clickhouse_data + ';')

    # Close connections
    postgres_cursor.close()
    postgres_conn.close()
    clickhouse_conn.disconnect()

if __name__ == '__main__':
    extract_load()