import sqlite3

DATABASE_NAME = 'database.db'


def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn


def create_db_table(conn=None):
    if conn is None:
        conn = connect_to_db(DATABASE_NAME)

    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS results (
                result_id INTEGER PRIMARY KEY NOT NULL,
                time_submitted TEXT NOT NULL
            );
        ''')
        conn.commit()
        print("results table created successfully")

    except sqlite3.Error as e:
        print(f"results table creation failed: {e}")

    finally:
        conn.close()


def insert_result(result, conn=None):
    inserted_result = {}

    if conn is None:
        conn = connect_to_db(DATABASE_NAME)

    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO results (time_submitted) VALUES (?)",
            (result['time_submitted'],)
        )
        conn.commit()
        inserted_result = get_result_by_id(cur.lastrowid, conn)

    except sqlite3.Error as e:
        conn.rollback()
        print(f"Insert failed: {e}")

    finally:
        conn.close()

    return inserted_result


def get_results():
    results = []
    conn = connect_to_db(DATABASE_NAME)

    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM results")
        rows = cur.fetchall()

        for i in rows:
            result = {}
            result["result_id"] = i["result_id"]
            result["time_submitted"] = i["time_submitted"]
            results.append(result)

    except sqlite3.Error as e:
        print(f"Query failed: {e}")

    finally:
        conn.close()

    return results


def get_result_by_id(result_id, conn=None):
    result = {}
    if conn is None:
        conn = connect_to_db(DATABASE_NAME)

    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM results WHERE result_id = ?", (result_id,))
        row = cur.fetchone()
        if row:
            result["result_id"] = row["result_id"]
            result["time_submitted"] = row["time_submitted"]

    except sqlite3.Error as e:
        print(f"Query by ID failed: {e}")

    finally:
        conn.close()

    return result
