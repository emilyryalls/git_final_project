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

def get_all_blogs():
    # establishing a connection with the database
    conn = get_db_connection()
    # cursor is a method that gives ability to interact with database
    cursor = conn.cursor()
    sql_get_all_blogs = "SELECT title, summary, image FROM blogs"
    # equivalent of clicking lightning bolt
    cursor.execute(sql_get_all_blogs)
    result = cursor.fetchall()
    blog_list = []

    for item in result:
        blog_list.append({'title': item[0],'summary': item[1],'image': item[2]})
    return blog_list






