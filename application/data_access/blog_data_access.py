import mysql.connector
import sys

# Set the MySQL password depending on the operating system
if sys.platform == "win32":
    mysql_password = "password"
else:
    mysql_password = ""

def get_db_connection():
    """
    Establishes a connection to the MySQL database 'rise_db'.

    Returns:
        MySQLConnection: A connection object to the database.
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=mysql_password,
        database="rise_db"
    )
    return mydb

# ------------------------- Get all blogs -------------------------
def get_all_blogs(category=None):
    """
    Retrieves all blog posts from the database, optionally filtered by category.
    Includes associated category and author information.

    Args:
        category (str, optional): The blog category to filter by. Defaults to None.

    Returns:
        list[dict]: A list of blog posts, each represented as a dictionary.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

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

    result = cursor.fetchall()

    if not result:
        print("No blogs found.")
        return []

    blog_list = []
    for item in result:
        blog_list.append({
            'blog_id': item[0],
            'title': item[1],
            'summary': item[2],
            'image': item[3],
            'category': item[4],
            'author_name': item[5]
        })

    return blog_list

# ------------------------ Get singular blog ------------------------
def get_blog_by_id(blog_id):
    """
    Retrieves a single blog post by its ID, including its full content and author details.

    Args:
        blog_id (int): The ID of the blog post to retrieve.

    Returns:
        dict or None: A dictionary of blog details if found, otherwise None.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT blog.blog_id, blog.title, blog.summary, blog.image, blog.content, 
                   blog_author.author_name, blog.created_at
            FROM blog 
            JOIN blog_author ON blog.author_id = blog_author.author_id
            WHERE blog.blog_id = %s
        """
        cursor.execute(query, (blog_id,))
        blog = cursor.fetchone()

        if blog is None:
            return None

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
        if conn:
            conn.close()
