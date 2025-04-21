import mysql.connector
import sys
import json
from datetime import datetime
from flask import session

# Determine MySQL password based on OS
if sys.platform == "win32":
    mysql_password = "password"
else:
    mysql_password = ""

def main():
    return None

def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.

    Returns:
        MySQLConnection: A connection object to the rise_db database.
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=mysql_password,
        database="rise_db"
    )
    return mydb

def get_user_id():
    """
    Retrieves the currently logged-in user's ID from the Flask session.

    Returns:
        int or None: The user_id if present in the session, else None.
    """
    return session.get("user_id")

def get_todays_meal_plan(user_id):
    """
    Retrieves the most recent meal plan for the user based on the current day of the week.

    Args:
        user_id (int): ID of the member.

    Returns:
        dict: A dictionary of meals for the current day, or an empty dict if no plan is found.
    """
    today = datetime.today().strftime('%A')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT meals 
        FROM meal_plans 
        WHERE member_id = %s 
        ORDER BY created_at DESC 
        LIMIT 1
    """, (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result and result['meals']:
        meals = json.loads(result['meals'])
        return meals.get(today, {})
    return {}

def get_member_goal_id(user_id):
    """
    Fetches the fitness goal ID for the specified user.

    Args:
        user_id (int): ID of the member.

    Returns:
        int or None: The goal_id if found, otherwise None.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT goal_id FROM member WHERE member_id = %s", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_todays_workout(user_id):
    """
    Retrieves today's workout plan for the user based on their goal and experience level.
    Splits compound exercise names into separate entries and includes reps and sets.

    Args:
        user_id (int): ID of the member.

    Returns:
        list[dict] or None: A list of workout dictionaries or None if user data is incomplete.
    """
    today = datetime.today().strftime('%A')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT goal_id, experience_id
        FROM member
        WHERE member_id = %s
    """, (user_id,))
    user_data = cursor.fetchone()

    if not user_data or not user_data['goal_id'] or not user_data['experience_id']:
        conn.close()
        return None

    goal_id = user_data['goal_id']
    experience_id = user_data['experience_id']

    cursor.execute("""
        SELECT e.exercise_name, x.reps, x.sets
        FROM exercise e
        JOIN day_of_week d ON e.day_id = d.day_id
        JOIN experience x ON x.experience_id = %s
        WHERE e.goal_id = %s AND d.day = %s
    """, (experience_id, goal_id, today))

    result = cursor.fetchall()
    conn.close()

    workout = []
    for row in result:
        for name in row['exercise_name'].split(','):
            workout.append({
                'exercise': name.strip(),
                'reps': row['reps'],
                'sets': row['sets']
            })

    return workout

def get_latest_blogs():
    """
    Retrieves the latest 3 blog posts with author details.

    Returns:
        list[dict]: A list of dictionaries, each representing a blog post.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            b.title,
            b.summary,
            b.image,
            a.author_name AS author,
            b.created_at
        FROM blog b
        JOIN blog_author a ON b.author_id = a.author_id
        ORDER BY b.created_at DESC
        LIMIT 3
    """)
    blogs = cursor.fetchall()
    conn.close()
    return blogs

def get_workout_progress_percent(user_id):
    """
    Calculates the percentage of workouts completed by the user for the current week (Mon–Sat).

    Args:
        user_id (int): ID of the member.

    Returns:
        int: Completion percentage out of 6 workout days.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) 
        FROM workout_progress 
        WHERE member_id = %s AND is_done = TRUE AND day_id BETWEEN 1 AND 6
    """, (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0]:
        return int((result[0] / 6) * 100)
    return 0

def get_days_of_week():
    """
    Retrieves the list of weekdays from the database.

    Returns:
        list[str]: List of day names (e.g. Monday, Tuesday).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT day FROM day_of_week")
    result = cursor.fetchall()
    conn.close()
    return [row[0] for row in result]

if __name__ == "__main__":
    main()
