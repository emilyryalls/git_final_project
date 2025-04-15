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
      database="rise_db1")
    return mydb


#                                               <----- Login ------>

def get_details_by_email(useremail):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_get_password_name = "SELECT hashed_password, first_name, email_address, member_id FROM v_login_details WHERE email_address = %s"
    cursor.execute(sql_get_password_name, (useremail,))

    saved_tuple = cursor.fetchone()
    return saved_tuple


#                                               <----- Add Member ------>

# <----- Add Member ------>
def add_member(fname, lname, uemail, hpassword):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if email already exists
    sql_check_email = "SELECT email_id FROM email WHERE email_address = %s"
    val_check = (uemail,)
    cursor.execute(sql_check_email, val_check)

    email_id = cursor.fetchone()

    if email_id:
        return True # Return true if email exist
    else:
        # Insert the input data into their tables executing the SQL queries
        sql_add_email = "INSERT INTO email (email_address) VALUES (%s)"
        val_email = (uemail,)
        cursor.execute(sql_add_email, val_email)
        conn.commit()

        # Get new user email_id
        cursor.execute(sql_check_email, (uemail,))
        new_email_id = cursor.fetchone()[0]


        sql_add_full_name = "INSERT INTO member (first_name, last_name, email_id) VALUES (%s, %s, %s)"
        val_full_name = (fname, lname, new_email_id)
        cursor.execute(sql_add_full_name, val_full_name)

        # Get new member_id
        sql_get_member_id = "SELECT member_id FROM member WHERE email_id = %s"
        val_member_id = (new_email_id,)
        cursor.execute(sql_get_member_id, val_member_id)
        new_member_id = cursor.fetchone()[0]

        sql_add_password = "INSERT INTO member_password (hashed_password, member_id) VALUES (%s, %s)"
        val_password = (hpassword, new_member_id)
        cursor.execute(sql_add_password, val_password)
        conn.commit()

