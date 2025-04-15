import mysql.connector
import sys
import os
import json

from unicodedata import category


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

#                                                   <---Meal planner --->

def get_user_meal_plans(user_id):
    # Mocking meal plans for testing
    return [
        {
            'user_id': user_id,
            'name': '05-04-2023',  # Example plan name
            'week': {
                'Monday': {'breakfast': 'Pancakes', 'lunch': 'Chicken Sandwich', 'dinner': 'Steak', 'snacks': 'Chips'},
                'Tuesday': {'breakfast': 'Oatmeal', 'lunch': 'Salad', 'dinner': 'Pizza', 'snacks': 'Fruit'},
                'Wednesday': {'breakfast': 'Eggs', 'lunch': 'Soup', 'dinner': 'Pasta', 'snacks': 'Nuts'},
                'Thursday': {'breakfast': 'Toast', 'lunch': 'Burger', 'dinner': 'Chicken Curry', 'snacks': 'Cookies'},
                'Friday': {'breakfast': 'Cereal', 'lunch': 'Tacos', 'dinner': 'Fish', 'snacks': 'Chips'},
                'Saturday': {'breakfast': 'Bagel', 'lunch': 'Pizza', 'dinner': 'BBQ', 'snacks': 'Granola'},
                'Sunday': {'breakfast': 'Waffles', 'lunch': 'Grilled Cheese', 'dinner': 'Roast Chicken', 'snacks': 'Fruit'}
            }
        }
    ]
