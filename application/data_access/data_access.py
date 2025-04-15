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


#                                               <----- Login ------>

def get_password_by_email(useremail):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_get_password = "SELECT user_password FROM member WHERE user_email = %s"
    cursor.execute(sql_get_password, (useremail,))

    saved_password_tuple = cursor.fetchone()
    return saved_password_tuple



#                                               <----- Add Member ------>
# def add_member(fname, lname, uemail, upassword):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#
#     #to be changed for real DB values
#     sql_check_email = "SELECT member_id FROM member WHERE user_email = %s"
#     cursor.execute(sql_check_email, (uemail,))
#
#     email_id = cursor.fetchone()
#
#     if email_id:
#         return True
#     else:
#         sql_add_member = "INSERT INTO member (firstname, lastname, user_email, user_password) VALUES (%s, %s, %s, %s)"
#         val = (fname, lname, uemail, upassword)
#
#     # try:
#     cursor.execute(sql_add_member, val)
#     conn.commit()
#     #print('added to db test')
#
#     # except mysql.connector.Error as err:
#     #     print(f"Error: {err}")
#     #
#     # finally:
#     #     cursor.close()
#     #     conn.close()
#
# #     def create():
# #         return mysql_password


def add_member(fname, lname, uemail, upassword):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Step 1. Check if the email already exists in the email table.
        sql_check_email = "SELECT email_id FROM email WHERE email_address = %s"
        cursor.execute(sql_check_email, (uemail,))
        email_row = cursor.fetchone()

        if email_row:
            email_id = email_row[0]
        else:
            # If email does not exist, insert it
            sql_add_email = "INSERT INTO email (email_address) VALUES (%s)"
            cursor.execute(sql_add_email, (uemail,))
            conn.commit()  # Commit to generate auto_increment value
            email_id = cursor.lastrowid

        # Step 2. Check if a member with this email_id already exists in the member table.
        sql_check_member = "SELECT member_id FROM member WHERE email_id = %s"
        cursor.execute(sql_check_member, (email_id,))
        member_row = cursor.fetchone()

        if member_row:
            # Member already exists
            return True  # or return an appropriate flag/value

        # Step 3. Insert the new member using the obtained email_id.
        # first_name, last_name, email_id, user_password
        sql_add_member = """
            INSERT INTO member (first_name, last_name, email_id, user_password)
            VALUES (%s, %s, %s, %s)
        """
        member_values = (fname, lname, email_id, upassword)
        cursor.execute(sql_add_member, member_values)
        conn.commit()

        return False  # Signify that the member was added successfully

    finally:
        cursor.close()
        conn.close()

