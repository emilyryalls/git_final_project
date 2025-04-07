import mysql.connector
import sys

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="blog_db")

if sys.platform == "win32":
    mysql_password = "password"
else:
    mysql_password = ""

