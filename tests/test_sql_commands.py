import pytest
import sqlite3
import os
from sql_commands import (
    connect_to_db, create_db_table, insert_result,
    get_results, get_result_by_id, DATABASE_NAME
)


@pytest.fixture
def setup_db():
    db_file = 'database.db'
    conn = sqlite3.connect(db_file)
    create_db_table(conn)  # Ensure the table is created
    yield db_file
    conn.close()
    os.remove(db_file)


@pytest.fixture
def connection(setup_db):
    conn = connect_to_db(setup_db)
    yield conn
    conn.close()


def test_create_db_table(setup_db):
    conn = connect_to_db(setup_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='results';")
    table = cursor.fetchone()
    assert table is not None
    assert table[0] == 'results'


def test_insert_result(setup_db):
    result = {'time_submitted': '2024-05-14 10:00:00'}
    inserted_result = insert_result(result)
    assert inserted_result['time_submitted'] == result['time_submitted']


def test_get_results(connection):
    result1 = {'time_submitted': '2024-05-14 10:00:00'}
    result2 = {'time_submitted': '2024-05-14 11:00:00'}
    insert_result(result1)
    insert_result(result2)
    results = get_results()
    assert len(results) == 2
    assert results[0]['time_submitted'] == result1['time_submitted']
    assert results[1]['time_submitted'] == result2['time_submitted']


def test_get_result_by_id(connection):
    result = {'time_submitted': '2024-05-14 10:00:00'}
    inserted_result = insert_result(result)
    result_id = inserted_result['result_id']
    retrieved_result = get_result_by_id(result_id)
    assert retrieved_result['result_id'] == result_id
    assert retrieved_result['time_submitted'] == result['time_submitted']
