import sqlite3
import json
from db.schema import SCHEMA_SQL

DB_NAME = "autodevcrew.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()

def save_task(description):
    init_db()  # Ensure DB is initialized
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (description) VALUES (?)", (description,))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id

def save_code(task_id, code):
    conn = get_connection()
    conn.execute("INSERT INTO generated_code (task_id, code) VALUES (?, ?)", (task_id, code))
    conn.commit()
    conn.close()

def save_test_log(task_id, test_results):
    conn = get_connection()
    conn.execute("INSERT INTO test_logs (task_id, test_results) VALUES (?, ?)", (task_id, test_results))
    conn.commit()
    conn.close()

def save_deployment_log(task_id, deployment_status):
    conn = get_connection()
    conn.execute("INSERT INTO deployment_logs (task_id, deployment_status) VALUES (?, ?)", (task_id, deployment_status))
    conn.commit()
    conn.close()

def save_final_report(task_id, summary):
    # summary is a dict, serialize it
    summary_json = json.dumps(summary)
    conn = get_connection()
    conn.execute("INSERT INTO final_reports (task_id, summary) VALUES (?, ?)", (task_id, summary_json))
    conn.commit()
    conn.close()

def get_task_summary(task_id):
    conn = get_connection()
    cursor = conn.execute("SELECT summary FROM final_reports WHERE task_id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row['summary'])
    return None
