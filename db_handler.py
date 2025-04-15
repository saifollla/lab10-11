import psycopg2

current_user = ''

conn = psycopg2.connect( # creating a connection
    host="localhost",
    database="snake_game",
    user="postgres",
    password="67890"
)

query_create_table_users = """
    CREATE TABLE users(
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE
    )
"""

query_create_table_user_scores = """
    CREATE TABLE user_scores(
        id SERIAL PRIMARY KEY,
        username VARCHAR(255),
        score INTEGER,
        level INTEGER
    )
"""


def execute_query(query):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def input_user():
    global current_user
    current_user = input("Enter the username: ")

def add_user(name):
    command = "INSERT INTO users (user_name) VALUES(%s)"
    try:
        with conn.cursor() as cur:
            cur.execute(command, (current_user,))
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def get_user_id(username):
    query_get_user_id = "SELECT user_id FROM users where user_name = %s"
    try:
        with conn.cursor() as cur:
            cur.execute(query_get_user_id, (current_user,))
            result = cur.fetchone()
            return int(result[0])
    except (psycopg2.DatabaseError, Exception) as error:
        print("fcp: ", error)

def check_if_user_exists(name):
    command = "SELECT user_name FROM users WHERE user_name = %s"
    try:
        with conn.cursor() as cur:
            cur.execute(command, (current_user,))
            result = cur.fetchall()
            return bool(result)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def add_new_score(username, score, level):
    command = "INSERT INTO user_score (user_id, score, level, speed) VALUES(%s, %s, %s, %s)"
    user_id = get_user_id(username)
    try:
        with conn.cursor() as cur:
            cur.execute(command, (user_id, score, level, score // 10 - 5,))
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def process_score(score):
    user_exists = check_if_user_exists(current_user)
    # print(user_exists)
    if not user_exists: 
        add_user(current_user)
    add_new_score(score)

def show_highest_score(current_user):
    command = "SELECT MAX(score) FROM user_score WHERE user_id = %s"
    try:
        with conn.cursor() as cur:
            cur.execute(command, (get_user_id(current_user),))
            result = cur.fetchone()
            return int(result[0])
    except (psycopg2.DatabaseError, Exception) as error:
        print("FCP2: ", error)
    

if __name__ == '__main__':
    input_user()
    process_score(10)
    # Create user and user_score tables. in the first run was created both users and user_score tables, now they are commented
    # execute_query(query_create_table_users)
    # execute_query(query_create_table_user_scores)