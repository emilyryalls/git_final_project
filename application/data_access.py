import mysql.connector
import sys

from unicodedata import category

if sys.platform == "win32":
    mysql_password = "password"
else:
    mysql_password = ""

def get_db_connection():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="password",
      database="blog_db")
    return mydb

# def get_all_blogs():
#     # establishing a connection with the database
#     conn = get_db_connection()
#     # cursor is a method that gives ability to interact with database
#     cursor = conn.cursor()
#     sql_get_all_blogs = "SELECT title, summary, image FROM blogs"
#     # equivalent of clicking lightning bolt
#     cursor.execute(sql_get_all_blogs)
#     result = cursor.fetchall()
#     blog_list = []
#
#     for item in result:
#         blog_list.append({'title': item[0],'summary': item[1],'image': item[2]})
#     return blog_list


def get_all_blogs(category=None):
    # Connect to the MySQL database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if a category was provided from the filter dropdown
    if category:
        # SQL query to fetch blogs that match the selected category
        sql_query_category = "SELECT title, summary, image FROM blogs WHERE category = %s"
        # Execute the query with category as parameter (MUST be a tuple)
        cursor.execute(sql_query_category, (category,))
    else:
        # If no category selected, fetch all blogs
        sql_query = "SELECT title, summary, image FROM blogs"
        cursor.execute(sql_query)

    # Fetch all results from the executed query
    result = cursor.fetchall()

    # Convert raw DB rows into a list of blog dictionaries
    blog_list = [{'title': item[0], 'summary': item[1], 'image': item[2]} for item in result]

    # Return the list
    return blog_list