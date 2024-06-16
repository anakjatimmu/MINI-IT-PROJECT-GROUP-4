import sqlite3
from datetime import datetime

def initialize_db():
    conn = sqlite3.connect("pomodoro_timer.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS profiles
                (name text, work_time integer, short_break_time integer, long_break_time integer)""")
    c.execute("""CREATE TABLE IF NOT EXISTS task
                (task text, work_time integer, short_break_time integer, long_break_time integer)""")
    conn.commit()
    conn.close()

def save_profile(profile_name, work_time, short_break_time, long_break_time):
    conn = sqlite3.connect("pomodoro_timer.db")
    c = conn.cursor()
    c.execute("INSERT INTO profiles (name, work_time, short_break_time, long_break_time) VALUES (?, ?, ?, ?)",
              (profile_name, work_time, short_break_time, long_break_time))
    conn.commit()
    conn.close()

def get_profiles():
    conn = sqlite3.connect("pomodoro_timer.db")
    c = conn.cursor()
    c.execute("SELECT * FROM profiles")
    profiles = c.fetchall()
    conn.close()
    return profiles

def update_profile(new_name, work_time, short_break_time, long_break_time, old_name):
    conn = sqlite3.connect("pomodoro_timer.db")
    c = conn.cursor()
    c.execute("""UPDATE profiles SET name =?, work_time =?, short_break_time =?, long_break_time =?
                WHERE name =?""", (new_name, work_time, short_break_time, long_break_time, old_name))
    conn.commit()
    conn.close()

def delete_profile(profile_name):
    conn = sqlite3.connect("pomodoro_timer.db")
    c = conn.cursor()
    c.execute("DELETE FROM profiles WHERE name=?", (profile_name,))
    conn.commit()
    conn.close()

def save_task(task, work_time, short_break_time, long_break_time):
    conn = sqlite3.connect("pomodoro_timer.db")
    c = conn.cursor()
    c.execute("INSERT INTO task (task, work_time, short_break_time, long_break_time) VALUES (?, ?, ?, ?)",
              (task, work_time, short_break_time, long_break_time))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect("pomodoro_timer.db")
    c = conn.cursor()
    c.execute("SELECT * FROM task")
    tasks = c.fetchall()
    conn.close()
    return tasks

def update_task(task, work_time, short_break_time, long_break_time):
    conn = sqlite3.connect("pomodoro_timer.db")
    c = conn.cursor()
    c.execute("""UPDATE task SET  task=?, work_time=?, short_break_time=?, long_break_time=?
                """, (task, work_time, short_break_time, long_break_time))
    conn.commit()
    conn.close()

def delete_task(task_name):
    conn = sqlite3.connect("pomodoro_timer.db")
    c = conn.cursor()
    c.execute("DELETE FROM task WHERE task=?", (task_name,))
    conn.commit()
    conn.close()