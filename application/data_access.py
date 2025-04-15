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
        sql_query_category = "SELECT id, title, summary, image FROM blog WHERE category = %s"
        # Execute the query with category as parameter (MUST be a tuple)
        cursor.execute(sql_query_category, (category,))
    else:
        # If no category selected, fetch all blogs
        sql_query = "SELECT id, title, summary, image FROM blog"
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
    cursor.execute("SELECT id, title, summary, image, content, author, created_at FROM blog WHERE id = %s", (blog_id,))

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



# <----- Login ------>

def get_password_by_email(useremail):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_get_password = "SELECT user_password FROM membership WHERE user_email = %s"
    cursor.execute(sql_get_password, (useremail,))

    saved_password_tuple = cursor.fetchone()
    return saved_password_tuple



# <----- Add Member ------>
def add_member(fname, lname, uemail, upassword):
    conn = get_db_connection()
    cursor = conn.cursor()

    #to be changed for real DB values
    sql_check_email = "SELECT id FROM membership WHERE user_email = %s"
    cursor.execute(sql_check_email, (uemail,))

    email_id = cursor.fetchone()

    if email_id:
        return True
    else:
        sql_add_member = "INSERT INTO membership (firstname, lastname, user_email, user_password) VALUES (%s, %s, %s, %s)"
        val = (fname, lname, uemail, upassword)

    # try:
    cursor.execute(sql_add_member, val)
    conn.commit()
    #print('added to db test')

    # except mysql.connector.Error as err:
    #     print(f"Error: {err}")
    #
    # finally:
    #     cursor.close()
    #     conn.close()




    def create():
        return mysql_password



















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
# optional filter parameters
# if none chosen will return all workout videos
def get_workout_video(goal=None, experience=None, time=None):
    """
    This function retrieves a list of workout videos from the database, optionally filtered by fitness goal,
    experience level, and time available. The function also formats each video link into an embeddable
    YouTube URL for display on the webpage.
    :param goal: str
    :param experience: str
    :param time: str
    :return: list of dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    # connect to database and create a cursor, used to execute SQL queries and fetch results

    # base query runs if no filters selected and returns all workout videos, and is appended later if filters are selected
    base_query = "SELECT video_name, video_link, fitness_goal, experience, time FROM v_workout_videos"
    filters = []

    # if filters selected on webpage, passed through function as parameters, added to the f string below (formatted to fit SQL query) and stored in filters list
    if goal:
        filters.append(f"fitness_goal = '{goal}'")
    if experience:
        filters.append(f"experience = '{experience}'")
    if time:
        filters.append(f"time = '{time}'")

    # if filters list not empty i.e. if any filters chosen
    if filters:
        conditions = " AND ".join(filters)
        base_query += " WHERE " + conditions
        # .join method takes the different elements in the filters list and makes a string using " AND " as the defined separator, and operator in SQL
        # spacing is important to make sure there are spaces between each condition
        # the new string made using the filters list is assigned to conditions
        # this is then appended to the base query, after " WHERE " (spacing again important) to use the SQL operator and apply conditions to the SQL query based on filters chosen on the webpage

    # run the final query and fetch the results
    cursor.execute(base_query)
    result = cursor.fetchall()
    # result is a list of tuples by default
    # each tuple represents a row from the database

    workout_video_list = []

    # for loop, for each tuple
    # first step is YouTube link taken from database, id extracted and inputted into correct string to embed YouTube videos, so that can be used in workout_videos.html
    # position 1 in each tuple (video_link, based on order SQL SELECT query) can be amended
    for item in result:
        video_link=item[1]
        video_id = get_youtube_video_id(video_link)
        embed_link = f"https://www.youtube.com/embed/{video_id}"

        # turn each tuple into a dictionary
        workout = {
            'video_name': item[0],
            'video_link': embed_link,
            'fitness_goal': item[2],
            'experience': item[3],
            'time': item[4]
        }
        workout_video_list.append(workout)
        # append the dictionary to the list
        #this is done for each tuple using the for loop

    return workout_video_list


def get_youtube_video_id(url):
    """
    This function takes a YouTube video URL and splits the string to separate the video id.
    The video id is needed to embed the YouTube video to a webpage.
    :param url: str
    :return: str
    """
    split_url = url.split('https://www.youtube.com/watch?v=')
    video_id = split_url[1]
    return video_id



