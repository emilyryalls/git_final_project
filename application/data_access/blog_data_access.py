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


#                                               <----- Get all blogs ----->
def get_all_blogs(category=None):
    # Connect to the MySQL database
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query to fetch blogs, including category and author, ordered by created_at
    if category:
        sql_query_category = """
            SELECT blog.blog_id, blog.title, blog.summary, blog.image, blog_category.category, blog_author.author_name 
            FROM blog 
            JOIN blog_category ON blog.category_id = blog_category.category_id
            JOIN blog_author ON blog.author_id = blog_author.author_id
            WHERE blog_category.category = %s
            ORDER BY blog.created_at DESC
        """
        cursor.execute(sql_query_category, (category,))
    else:
        sql_query = """
            SELECT blog.blog_id, blog.title, blog.summary, blog.image, blog_category.category, blog_author.author_name 
            FROM blog
            JOIN blog_category ON blog.category_id = blog_category.category_id
            JOIN blog_author ON blog.author_id = blog_author.author_id
            ORDER BY blog.created_at DESC
        """
        cursor.execute(sql_query)

    # Fetch all results from the executed query
    result = cursor.fetchall()

    # Check if any blogs were returned
    if not result:
        print("No blogs found.")
        return []

    blog_list = []
    # Convert raw DB rows into a list of blog dictionaries
    for item in result:
        blog_list.append({
            'blog_id': item[0],
            'title': item[1],
            'summary': item[2],
            'image': item[3],
            'category': item[4],  # Include category if needed
            'author_name': item[5]  # Add author name
        })

    # Return the list of blogs
    return blog_list

#                                               <----- Get singular blog ------>
def get_blog_by_id(blog_id):
    """
    Fetches a blog post by its ID, including the author's name.
    Returns the blog details as a dictionary, or None if not found.
    """
    try:
        # Establish a connection to the database
        conn = get_db_connection()

        # Use a cursor to interact with the database
        cursor = conn.cursor()

        # Query to fetch the blog and its author information
        query = """
            SELECT blog.blog_id, blog.title, blog.summary, blog.image, blog.content, 
                   blog_author.author_name, blog.created_at
            FROM blog 
            JOIN blog_author ON blog.author_id = blog_author.author_id
            WHERE blog.blog_id = %s
        """

        # Execute the query
        cursor.execute(query, (blog_id,))

        # Fetch the result
        blog = cursor.fetchone()

        # If no blog is found, return None
        if blog is None:
            return None

        # Return the blog details as a dictionary
        return {
            'blog_id': blog[0],
            'title': blog[1],
            'summary': blog[2],
            'image': blog[3],
            'content': blog[4],
            'author_name': blog[5],
            'created_at': blog[6].strftime('%B %d, %Y')
        }

    except mysql.connector.Error as err:
        print(f"Error occurred while fetching blog: {err}")
        return None

    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()


