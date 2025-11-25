from db import get_connection

def create_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
    conn.commit()
    cur.close()
    conn.close()

def get_user_by_username(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT username, password FROM users WHERE username = %s', (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {'username': row[0], 'password': row[1]}
    return None