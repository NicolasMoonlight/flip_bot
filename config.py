import os, sqlite3
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

DB_NAME = 'flip.sqlite3'
db_path = os.path.join(os.getcwd(), DB_NAME)

# if the file does not exist, it creates it and connects, otherwise it just connects
if not os.path.isfile(db_path):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE users
                (user text, heads text, tails text)''')

    conn.commit()
else:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

# gets statistic flips of user
def get_stats_user(user_id):
    c.execute(rf"SELECT heads, tails FROM users WHERE user={user_id}")
    return c.fetchone()

# set new flips values of user
def set_user_values(user_id: int, value: str):
    c.execute(rf"SELECT {value} FROM users WHERE user={user_id}")
    set_value = int(c.fetchall()[0][0]) + 1

    c.execute(rf"UPDATE users SET {value} = ? WHERE user = ?", (set_value, user_id))
    conn.commit()

# checks if there is a player in the database
def check_user(user_id: int):
    c.execute(rf"SELECT * FROM users WHERE user={user_id}")
    if c.fetchone() is not None:
        return True
    else:
        return False

# creates a new user in the database
def create_new_user(user_id: int):
    c.execute(rf"INSERT INTO users (user, heads, tails) VALUES ({user_id}, 0, 0)")
    conn.commit()