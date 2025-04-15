import mysql.connector
import sys
import os
import json
from flask import session

if sys.platform == "win32":
    mysql_password = "password"
else:
    mysql_password = ""

def get_db_connection():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password= mysql_password,
      database="rise_db")
    return mydb

# Directory to store user meal plans
USER_MEAL_PLANS_DIR = r'C:\Code\project\git_final_project\application\user_meal_plans'
MAX_MEAL_PLANS = 4

#                                                   <---Meal planner --->


def get_user_id():
    return session.get('user_id')

def generate_plan_filename(user_id, created_at):
    return f'{user_id}_meal_plan_{created_at}.json'

def get_user_plan_files(user_id):
    return sorted([
        f for f in os.listdir(USER_MEAL_PLANS_DIR)
        if f.startswith(f'{user_id}_meal_plan')
    ], key=lambda x: os.path.getctime(os.path.join(USER_MEAL_PLANS_DIR, x)))

def save_plan_to_file(user_id, plan):
    created_at = plan['created_at']
    filename = generate_plan_filename(user_id, created_at)
    filepath = os.path.join(USER_MEAL_PLANS_DIR, filename)

    with open(filepath, 'w') as f:
        json.dump(plan, f, indent=4)

    # Clean up old plans if more than max allowed
    user_files = get_user_plan_files(user_id)
    if len(user_files) > MAX_MEAL_PLANS:
        oldest_file = os.path.join(USER_MEAL_PLANS_DIR, user_files[0])
        os.remove(oldest_file)

    return filepath

def load_latest_plan(user_id):
    user_files = get_user_plan_files(user_id)
    if not user_files:
        return None
    latest_file = os.path.join(USER_MEAL_PLANS_DIR, user_files[-1])
    with open(latest_file, 'r') as f:
        return json.load(f)