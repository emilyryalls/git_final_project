import mysql.connector
import sys

if sys.platform == "win32":
    mysql_password = "password"
else:
    mysql_password = ""