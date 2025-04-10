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
      password= mysql_password,
      database="blog_db")
    return mydb

# <----- Orignal get all blogs. We no longer need this ----->
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

    # Convert raw DB rows into a list of blog dictionaries
    blog_list = [{'id': item[0], 'title': item[1], 'summary': item[2], 'image': item[3]} for item in result]

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