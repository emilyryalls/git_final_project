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


# <----- Get all blog function ----->
# def get_all_blogs(category=None):
#     # Connect to the MySQL database
#     conn = get_db_connection()
#     cursor = conn.cursor()
#
#     # Check if a category was provided from the filter dropdown
#     if category:
#         # SQL query to fetch blogs that match the selected category
#         sql_query_category = "SELECT id, title, summary, image FROM blogs WHERE category = %s"
#         # Execute the query with category as parameter (MUST be a tuple)
#         cursor.execute(sql_query_category, (category,))
#     else:
#         # If no category selected, fetch all blogs
#         sql_query = "SELECT id, title, summary, image FROM blogs"
#         cursor.execute(sql_query)
#
#     # Fetch all results from the executed query
#     result = cursor.fetchall()
#
#     blog_list = []
#     # Convert raw DB rows into a list of blog dictionaries
#     for item in result:
#         blog_list.append({'id': item[0], 'title': item[1], 'summary': item[2], 'image': item[3]})
#
#     # Return the list
#     return blog_list
#
#
# # <----- Get singular blog ------>
# def get_blog_by_id(blog_id):
#     # Establish a connection to the database
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     # Execute the query to get the blog based on the blog ID
#     cursor.execute("SELECT id, title, summary, image, content, author, created_at FROM blogs WHERE id = %s", (blog_id,))
#
#     # Fetch the result
#     blog = cursor.fetchone()
#     # Close the connection to the database
#     conn.close()
#
#     # If no blog is found, return None
#     if blog is None:
#         return None
#     # Return the blog details as a dictionary
#     return {'id': blog[0], 'title': blog[1], 'summary': blog[2], 'image': blog[3], 'content': blog[4], 'author' : blog[5], 'created_at': blog[6].date().strftime('%B %d, %Y')
#     }



# <----- Login ------>

def get_password_email_by_email(useremail):
    conn = get_db_connection()
    cursor = conn.cursor()

    # sql_get_password = "SELECT user_password FROM membership WHERE user_email = %s"
    # cursor.execute(sql_get_password, (useremail,))
    #
    # saved_password_tuple = cursor.fetchone()
    # return saved_password_tuple


    sql_get_password_name = "SELECT hashed_password, first_name, email_address FROM v_login_details WHERE email_address = %s"
    cursor.execute(sql_get_password_name, (useremail,))

    saved_tuple = cursor.fetchone()
    return saved_tuple



# <----- Add Member ------>
def add_member(fname, lname, uemail, hpassword):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if email already exists
    sql_check_email = "SELECT email_id FROM email WHERE email_address = %s"
    val_check = (uemail,)
    cursor.execute(sql_check_email, val_check)

    email_id = cursor.fetchone()

    if email_id:
        return True # Return true if email exist
    else:
        # Insert the input data into their tables executing the SQL queries
        sql_add_email = "INSERT INTO email (email_address) VALUES (%s)"
        val_email = (uemail,)
        cursor.execute(sql_add_email, val_email)
        conn.commit()

        # Get new user email_id
        cursor.execute(sql_check_email, (uemail,))
        new_email_id = cursor.fetchone()[0]


        sql_add_full_name = "INSERT INTO member (first_name, last_name, email_id) VALUES (%s, %s, %s)"
        val_full_name = (fname, lname, new_email_id)
        cursor.execute(sql_add_full_name, val_full_name)

        # Get new member_id
        sql_get_member_id = "SELECT member_id FROM member WHERE email_id = %s"
        val_member_id = (new_email_id,)
        cursor.execute(sql_get_member_id, val_member_id)
        new_member_id = cursor.fetchone()[0]

        sql_add_password = "INSERT INTO member_password (hashed_password, member_id) VALUES (%s, %s)"
        val_password = (hpassword, new_member_id)
        cursor.execute(sql_add_password, val_password)
        conn.commit()






















# <---Meal planner --->
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


# <---Workout Videos --->
def get_workout_video(goal=None, experience=None, time=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    if goal:
        sql_query_goal = "SELECT video_name, video_link, fitness_goal, experience, time FROM v_workout_videos WHERE goal = %s"
        cursor.execute(sql_query_goal, (goal,))

    elif experience:
        sql_query_experience = "SELECT video_name, video_link, fitness_goal, experience, time FROM v_workout_videos WHERE experience = %s"
        cursor.execute(sql_query_experience, (experience,))

    elif time:
        sql_query_time = "SELECT video_name, video_link, fitness_goal, experience, time FROM v_workout_videos WHERE time = %s"
        cursor.execute(sql_query_time, (time,))

    else:
        sql_query = "SELECT video_name, video_link, fitness_goal, experience, time FROM v_workout_videos"
        cursor.execute(sql_query)

    result = cursor.fetchall()
    workout_video_list = []
    for item in result:
        workout_video_list.append({'video_name': item[0], 'video_link': item[1], 'fitness_goal': item[2], 'experience': item[3], 'time': item[4]})

    return workout_video_list

