import sqlite3


def get_db():
    conn = sqlite3.connect('EasyPunchCard.db')
    return conn

def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS all_users (
                   student_id TEXT PRIMARY KEY,
                   username TEXT NOT NULL,
                   admin_status INT NOT NULL,
                   total_minutes INT
                   )
                   ''')
    conn.commit()
    cursor.close()
    conn.close()


def add_user(student_id:str, username:str, admin_status:int):
    conn = get_db()
    cursor = conn.cursor()
    # Add user into main table
    # total_minutes will always start at 0 for users inserted into all_users
    cursor.execute(f'''
                    INSERT INTO all_users(student_id, username, admin_status, total_minutes)
                    VALUES('{student_id}', '{username}', {admin_status}, 0)
                    ''')
    # create table for user
    cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS user_{student_id} (
                    student_id TEXT,
                    date TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    total_minutes INT,
                    CONSTRAINT FK_student_id FOREIGN KEY (student_id)
                    REFERENCES all_users(student_id)
                    )
                    ''')
    conn.commit()
    cursor.close()
    conn.close()

create_table()
add_user("007812423", "John Doe", 0)