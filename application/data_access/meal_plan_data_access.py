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
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=mysql_password,
        database="rise_db1"
    )

# Get current user's ID from session
def get_user_id():
    return session.get('user_id')

# Week start calculation
def get_week_start_date(date=None):
    if not date:
        date = datetime.now()
    return date - timedelta(days=date.weekday())

# Load the 4 most recent meal plans from DB
def load_user_meal_plans(user_id):
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
