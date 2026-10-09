import psycopg2

def db_connection(db_config: dict[str, str]) -> object:
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    cur.execute("SELECT 1")
    response = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return response
