import psycopg2
from config import load_config

def check_user(username):
    query = "SELECT user_id FROM users WHERE user_name = %s"

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (username,))
                result = cur.fetchone()
                if result:
                    user_id = result[0]
                    print(f"Welcome back, {username}.")
                    return user_id
                else:
                    print(f"User {username} does not exist. Please register.")
                    return None
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return None


def register_user(username):
    query = "INSERT INTO users (user_name) VALUES (%s) RETURNING user_id"
    
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (username,))
                user_id = cur.fetchone()[0]
                print(f"User {username} registered successfully.")
                return user_id
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return None


def load_user_score(user_id):
    query = "SELECT score, level, speed FROM user_score WHERE user_id = %s"

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (user_id,))
                result = cur.fetchone()
                if result:
                    score, level, speed = result
                    print(f"Current score: {score}, Level: {level}, Speed: {speed}")
                    return score, level, speed
                else:
                    print("No score data found. Starting a new game.")
                    return 0,0,0
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return 0
    

def game_loop():
    username = input("Enter username: ")

    # Checks if user exists
    user_id = check_user(username)
    if not user_id:
        user_id = register_user(username)  # Register new user if not found

    # Load user score and level
    load_user_score(user_id)


if __name__ == '__main__':
    game_loop()
