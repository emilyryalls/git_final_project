import mysql.connector
import sys

import mysql.connector
import sys


if sys.platform == "win32":
    mysql_password = "password"
else:
    mysql_password = ""

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=mysql_password,
  database="rise_db"
)

def get_db_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=mysql_password,
        database="rise_db"
    )
    return mydb

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, firstname, dob, height, weight, goal, member_since
        FROM users
        WHERE id = %s
    """, (user_id,))

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        return {
            "id": row[0],
            "firstname": row[1],
            "dob": row[2],
            "height": row[3],
            "weight": row[4],
            "goal": row[5],
            "member_since": row[6]
        }
    else:
        return None


def update_profile_info(user_id, dob, height, weight, goal):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET dob = %s, height = %s, weight = %s, goal = %s
        WHERE id = %s
    """, (dob, height, weight, goal, user_id))
    conn.commit()
    cursor.close()
    conn.close()
