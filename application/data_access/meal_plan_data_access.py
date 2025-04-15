import mysql.connector
import sys
import os
import json
from flask import session
from datetime import datetime, timedelta


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
MAX_MEAL_PLANS = 6


def get_user_id():
    return session.get('user_id')


def generate_plan_filename(user_id, created_at):
    """Generate a filename for a user's meal plan based on the user_id and timestamp."""
    return f'{user_id}_meal_plan_{created_at}.json'


def get_week_start_date(date=None):
    """Get the Monday of the week for the given date or today."""
    if not date:
        date = datetime.now()
    return date - timedelta(days=date.weekday())  # Monday is weekday 0


def find_meal_plan_by_timestamp(user_id, timestamp):
    for filename in get_user_plan_files(user_id):
        with open(os.path.join(USER_MEAL_PLANS_DIR, filename), 'r') as f:
            data = json.load(f)
            if data.get('created_at') == timestamp:
                return data
    return None


def get_user_plan_files(user_id):
    """Return a sorted list of meal plan filenames for a given user."""
    return sorted([
        f for f in os.listdir(USER_MEAL_PLANS_DIR)
        if f.startswith(f'{user_id}_meal_plan')
    ], key=lambda x: os.path.getctime(os.path.join(USER_MEAL_PLANS_DIR, x)))


def save_plan_to_file(user_id, plan):
    """Save the user's meal plan to a file. Automatically cleans up old files if more than MAX_MEAL_PLANS."""
    created_at = plan['created_at']
    filename = generate_plan_filename(user_id, created_at)
    filepath = os.path.join(USER_MEAL_PLANS_DIR, filename)

    # Save meal plan to file
    with open(filepath, 'w') as f:
        json.dump(plan, f, indent=6)

    # Cleanup old meal plans if more than MAX_MEAL_PLANS
    user_files = get_user_plan_files(user_id)
    if len(user_files) > MAX_MEAL_PLANS:
        oldest_file = os.path.join(USER_MEAL_PLANS_DIR, user_files[0])
        os.remove(oldest_file)

    return filepath


def load_latest_plan(user_id):
    """Load the most recent meal plan for a user."""
    user_files = get_user_plan_files(user_id)
    if not user_files:
        return None

    latest_file = os.path.join(USER_MEAL_PLANS_DIR, user_files[-1])
    with open(latest_file, 'r') as f:
        return json.load(f)


def load_plan_by_timestamp(user_id, timestamp):
    """Load a specific meal plan by its timestamp."""
    user_files = get_user_plan_files(user_id)
    for filename in user_files:
        if timestamp in filename:  # If the filename contains the timestamp, load it
            filepath = os.path.join(USER_MEAL_PLANS_DIR, filename)
            with open(filepath, 'r') as f:
                return json.load(f)
    return None