import sqlite3
import pandas as pd

def connect():
    # Keep the timeout to prevent "Database is locked" errors
    return sqlite3.connect("tracker.db", check_same_thread=False, timeout=5)

def init_db():
    with connect() as conn:
        cursor = conn.cursor()

        # 1. Dashboard Goals Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, category TEXT, mode TEXT, 
            time_value TEXT, duration INTEGER, completed BOOLEAN
        )""")

        # 2. Mission Planning Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, category TEXT, mode TEXT, 
            time_value TEXT, duration INTEGER, completed BOOLEAN
        )""")

        # 3. Goal/Mission Details (Intel)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS goal_details (
            goal_id INTEGER,
            section TEXT,
            content TEXT,
            PRIMARY KEY (goal_id, section)
        )""")

        # 4. Tasks Table (Unified structure with mission_id)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mission_id INTEGER,
            task TEXT, 
            date TEXT, 
            completed BOOLEAN
        )""")

        # 5. Habits Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE, wake_time TEXT, sleep_time TEXT,
            water REAL, steps INTEGER, workout TEXT, walk BOOLEAN,
            screen_time REAL, mood INTEGER, energy INTEGER, 
            focus INTEGER, meals INTEGER, snacks INTEGER, night_issue TEXT
        )""")

        # 6. Supporting Tables
        cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, note TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS wishlist (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, completed BOOLEAN)")
        cursor.execute("CREATE TABLE IF NOT EXISTS period (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, flow TEXT, mood TEXT, notes TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS routines (id INTEGER PRIMARY KEY AUTOINCREMENT, day TEXT, start_time TEXT, end_time TEXT, task TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS yearly_goals (id INTEGER PRIMARY KEY AUTOINCREMENT, goal TEXT, completed BOOLEAN)")
        
        conn.commit()


def add_mission(title, category, mode, time_value, duration):
    with connect() as conn:
        conn.execute("""
            INSERT INTO missions (title, category, mode, time_value, duration, completed)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, category, mode, str(time_value), duration, False))

def delete_mission(mission_id):
    with connect() as conn:
        conn.execute("DELETE FROM missions WHERE id=?", (mission_id,))
        conn.execute("DELETE FROM goal_details WHERE goal_id=?", (mission_id,))

def add_goal(title, category, mode, time_value, duration):
    with connect() as conn:
        conn.execute("""
            INSERT INTO goals (title, category, mode, time_value, duration, completed)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, category, mode, str(time_value), duration, False))

def delete_goal(goal_id):
    with connect() as conn:
        conn.execute("DELETE FROM goals WHERE id=?", (goal_id,))
        conn.execute("DELETE FROM goal_details WHERE goal_id=?", (goal_id,))

def save_goal_detail(goal_id, section, content):
    with connect() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO goal_details (goal_id, section, content)
            VALUES (?, ?, ?)
        """, (goal_id, section, content))


def add_task(task, task_date, mission_id=None):
    with connect() as conn:
        conn.execute("""
            INSERT INTO tasks (task, date, mission_id, completed) 
            VALUES (?, ?, ?, ?)
        """, (task, str(task_date), mission_id, False))

def load_tasks_by_date(task_date):
    with connect() as conn:
        return conn.execute(
            "SELECT * FROM tasks WHERE date = ? ORDER BY completed ASC, task ASC", 
            (str(task_date),)
        ).fetchall()

def update_task_status(task_id, status):
    with connect() as conn:
        conn.execute("UPDATE tasks SET completed=? WHERE id=?", (status, task_id))

def delete_task(task_id):
    with connect() as conn:
        conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))


def save_habits(date, wake, sleep, water, steps, workout, walk, screen, mood, energy, focus, meals, snacks, night_issue):
    with connect() as conn:
        conn.execute("""
        INSERT OR REPLACE INTO habits (
            date, wake_time, sleep_time, water, steps, workout, walk,
            screen_time, mood, energy, focus, meals, snacks, night_issue
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (date, wake, sleep, water, steps, workout, walk, screen, mood, energy, focus, meals, snacks, night_issue))


def add_wishlist(item):
    with connect() as conn:
        conn.execute("INSERT INTO wishlist (item, completed) VALUES (?, ?)", (item, False))

def update_wishlist(item_id, status):
    with connect() as conn:
        conn.execute("UPDATE wishlist SET completed=? WHERE id=?", (status, item_id))

def delete_wishlist(item_id):
    with connect() as conn:
        conn.execute("DELETE FROM wishlist WHERE id=?", (item_id,))

def load_wishlist():
    with connect() as conn:
        return pd.read_sql_query("SELECT * FROM wishlist", conn)