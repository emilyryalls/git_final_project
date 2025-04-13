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
def get_all_blogs(category=None):
    # Connect to the MySQL database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if a category was provided from the filter dropdown
    if category:
        # SQL query to fetch blogs that match the selected category
        sql_query_category = "SELECT id, title, summary, image FROM blogs WHERE category = %s"
        # Execute the query with category as parameter (MUST be a tuple)
        cursor.execute(sql_query_category, (category,))
    else:
        # If no category selected, fetch all blogs
        sql_query = "SELECT id, title, summary, image FROM blogs"
        cursor.execute(sql_query)

    # Fetch all results from the executed query
    result = cursor.fetchall()

    blog_list = []
    # Convert raw DB rows into a list of blog dictionaries
    for item in result:
        blog_list.append({'id': item[0], 'title': item[1], 'summary': item[2], 'image': item[3]})

    # Return the list
    return blog_list


# <----- Get singular blog ------>
def get_blog_by_id(blog_id):
    # Establish a connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    # Execute the query to get the blog based on the blog ID
    cursor.execute("SELECT id, title, summary, image, content, author, created_at FROM blogs WHERE id = %s", (blog_id,))

    # Fetch the result
    blog = cursor.fetchone()
    # Close the connection to the database
    conn.close()

    # If no blog is found, return None
    if blog is None:
        return None
    # Return the blog details as a dictionary
    return {'id': blog[0], 'title': blog[1], 'summary': blog[2], 'image': blog[3], 'content': blog[4], 'author' : blog[5], 'created_at': blog[6].date().strftime('%B %d, %Y')
    }

# <----- Add Member ------>
def add_member(uemail, upassword):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_add_member = "INSERT INTO membership (user_email, user_password) VALUES (%s, %s)"
    val = (uemail, upassword)

    try:
        cursor.execute(sql_add_member, val)
        conn.commit()
        print('added to db test')

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        conn.close()

# def add_member(uemail, upassword):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#
#     #checkk if email exist
#     sql_check_colour = "SELECT id FROM membership WHERE user_email = %s" # the %s the s is for string
#     cursor.execute(sql_check_colour, (email,)) ## execute above query passing the colour to the placeholder %s
#
#     email_result = cursor.fetchone()
#
#     if email_result: # if true then save it in below variable
#         email_id = email_result[0]
#     else:
#         sql_add_member = "INSERT INTO membership (user_email, user_password) VALUES (%s, %s)"
#         val = (uemail, upassword)
#     try:
#         cursor.execute(sql_add_member, val)
#         conn.commit()
#         print('added to db test')
#
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#
#     finally:
#         cursor.close()
#         conn.close()


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

