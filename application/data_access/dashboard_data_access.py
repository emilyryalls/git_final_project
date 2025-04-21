import mysql.connector
import sys
import json
from datetime import datetime
from flask import session

if sys.platform == "win32":
    mysql_password = "password"
else:
    mysql_password = ""

def main():
    return None

def get_db_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=mysql_password,
        database="rise_db"
    )
    return mydb


# 1. Get current user ID from session
def get_user_id():
    return session.get("user_id")

# 2. Get today's meal plan (latest plan, current day only)
def get_todays_meal_plan(user_id):
    # remove next 3 lines to remove hardcoding/testing and remove date=None arg in function
    # if date is None:
    #     date = datetime.today().date()
    # today = date.strftime('%A')

    # uncomment this
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

# 3. Get member's fitness goal ID
def get_member_goal_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT goal_id FROM member WHERE member_id = %s", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# 4. Get today’s workout plan (exercise names)
def get_todays_workout(user_id):
    today = datetime.today().strftime('%A')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get the user's goal and experience ID
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

    # Now get today's exercises + reps/sets based on experience
    cursor.execute("""
        SELECT e.exercise_name, x.reps, x.sets
        FROM exercise e
        JOIN day_of_week d ON e.day_id = d.day_id
        JOIN experience x ON x.experience_id = %s
        WHERE e.goal_id = %s AND d.day = %s
    """, (experience_id, goal_id, today))

    result = cursor.fetchall()
    conn.close()

    # Split exercises into individual items
    workout = []
    for row in result:
        for name in row['exercise_name'].split(','):
            workout.append({
                'exercise': name.strip(),
                'reps': row['reps'],
                'sets': row['sets']
            })

    return workout

# 5. Get latest 3 blog posts
def get_latest_blogs():
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

# 6. Get % progress for the week (6 workout days)
def get_workout_progress_percent(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Only count completed days from Monday to Saturday (day_id 1 to 6)
    cursor.execute("""
        SELECT COUNT(*) 
        FROM workout_progress 
        WHERE member_id = %s AND is_done = TRUE AND day_id BETWEEN 1 AND 6
    """, (user_id,))

    result = cursor.fetchone()
    conn.close()

    if result and result[0]:
        return int((result[0] / 6) * 100)  # Always divide by 6 (not result[1] or total)
    return 0

# 7. Get full list of weekdays (for reference)
def get_days_of_week():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT day FROM day_of_week")
    result = cursor.fetchall()
    conn.close()
    return [row[0] for row in result]


if __name__ == "__main__":
    main()
