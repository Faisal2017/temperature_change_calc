#!/usr/bin/python
import sqlite3
import json


def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn


def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS results (
                result_id INTEGER PRIMARY KEY NOT NULL,
                time_submitted TEXT NOT NULL
            );
        ''')

        conn.commit()
        print("results table created successfully")
    except:
        print("results table creation failed - Maybe table")
    finally:
        conn.close()


def insert_result(result):
    inserted_result = {}

    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO results (time_submitted)"
            "VALUES (?)",
            (result['time_submitted'],)
        )

        conn.commit()
        inserted_result = get_result_by_id(cur.lastrowid)

    except:
        conn().rollback()

    finally:
        conn.close()

    return inserted_result


def get_results():
    results = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM results")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            user = {}
            user["result_id"] = i["result_id"]
            user["time_submitted"] = i["time_submitted"]

            results.append(user)

    except:
        results = []

    return results

def get_result_by_id(result_id):
    result = {}

    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM results WHERE result_id = ?",
                       (result_id,))

        row = cur.fetchone()

        # convert row object to dictionary
        result["result_id"] = row["result_id"]
        result["time_submitted"] = row["time_submitted"]

    except:
        result = {}

    return result