import mysql.connector
import sys
import os
import json
from flask import session
from datetime import datetime, timedelta

# Handle MySQL password based on platform
if sys.platform == "win32":
    mysql_password = "password"
else:
    mysql_password = ""


# MySQL connection
def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: The database connection object.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=mysql_password,
        database="rise_db"
    )


# Get current user's ID from session
def get_user_id():
    """
    Retrieves the currently logged-in user's ID from the Flask session.

    Returns:
        int or None: The user ID if available, otherwise None.
    """
    return session.get('user_id')


# Week start calculation
def get_week_start_date(date=None):
    """
    Calculates the start date (Monday) of the week for a given date.

    Args:
        date (datetime, optional): A specific date. Defaults to today if not provided.

    Returns:
        datetime: The date of the Monday of the week.
    """
    if not date:
        date = datetime.now()
    return date - timedelta(days=date.weekday())


# Load the 4 most recent meal plans from DB
def load_user_meal_plans(user_id):
    """
    Retrieves the 4 most recent meal plans for a specific user.

    Args:
        user_id (int): The user's ID.

    Returns:
        list: A list of dictionaries, each containing meal plan details.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT name, created_at, description, meals
        FROM meal_plans
        WHERE member_id = %s
        ORDER BY created_at DESC
        LIMIT 4
    """, (user_id,))

    results = cursor.fetchall()
    conn.close()

    meal_plans = []
    for row in results:
        meal_plans.append({
            'name': row['name'],
            'created_at': row['created_at'],
            'timestamp': row['created_at'],  # for URL usage
            'description': row['description'],
            'meals': json.loads(row['meals']) if isinstance(row['meals'], str) else row['meals']
        })

    return meal_plans


# Find a specific meal plan by timestamp from DB
def find_meal_plan_by_timestamp(user_id, timestamp):
    """
    Finds and returns a specific meal plan by its creation timestamp.

    Args:
        user_id (int): The user's ID.
        timestamp (datetime): The creation timestamp of the meal plan.

    Returns:
        dict or None: The meal plan data as a dictionary if found, otherwise None.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT name, created_at, description, meals
        FROM meal_plans
        WHERE member_id = %s AND created_at = %s
        LIMIT 1
    """, (user_id, timestamp))

    result = cursor.fetchone()
    conn.close()

    if result:
        # Convert meals from JSON string to Python dict
        meals_data = result['meals']
        if isinstance(meals_data, str):
            try:
                meals_data = json.loads(meals_data)
            except json.JSONDecodeError:
                meals_data = {}  # fallback if it's broken

        return {
            'user_id': user_id,
            'name': result['name'],
            'created_at': result['created_at'],
            'description': result['description'],
            'meals': meals_data
        }

    return None


# Save a new meal plan to the database
def save_meal_plan_to_db(user_id, plan):
    """
    Saves a new meal plan to the database for a specific user.

    Args:
        user_id (int): The user's ID.
        plan (dict): A dictionary containing the meal plan data.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    meals_json = json.dumps(plan['meals']) if 'meals' in plan else json.dumps(plan['week'])

    cursor.execute("""
        INSERT INTO meal_plans (member_id, name, description, meals, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        user_id,
        plan['name'],
        plan.get('description', ''),
        meals_json,
        plan['created_at']
    ))

    conn.commit()
    conn.close()


# Update an existing meal plan
def update_meal_plan_in_db(user_id, timestamp, updated_plan):
    """
    Updates an existing meal plan in the database using the timestamp as a unique identifier.

    Args:
        user_id (int): The user's ID.
        timestamp (datetime): The creation timestamp of the meal plan to update.
        updated_plan (dict): A dictionary containing the updated meal plan data.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    meals_json = json.dumps(updated_plan['meals'])

    cursor.execute("""
        UPDATE meal_plans
        SET name = %s, description = %s, meals = %s
        WHERE member_id = %s AND created_at = %s
    """, (
        updated_plan['name'],
        updated_plan.get('description', ''),
        meals_json,
        user_id,
        timestamp
    ))

    conn.commit()
    conn.close()
