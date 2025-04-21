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
# Returns user details tuple or None
def get_details_by_email(useremail):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql_get_password_name = "SELECT hashed_password, first_name, email_address, member_id, email_id FROM v_login_details WHERE email_address = %s"
        cursor.execute(sql_get_password_name, (useremail,))
        saved_tuple = cursor.fetchone()

    # We are not using except here because we are already handling that logic in the routes
    finally:        # Ensure cursor and connection are closed, even if an error occurs
        cursor.close()
        conn.close()
    return saved_tuple

#                                               <----- Add Member ------>

# <----- Add Member ------>
def add_member(fname, lname, uemail, hpassword):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
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

    finally:
        cursor.close()
        conn.close()


#####
def get_password_details_by_id(memberid):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql_get_password_id = "SELECT hashed_password FROM v_login_details WHERE member_id = %s"
        cursor.execute(sql_get_password_id, (memberid,))
        saved_tuple = cursor.fetchone()
        return saved_tuple

    finally:
        cursor.close()
        conn.close()

# Returns True if password updated successfully
def change_password(hashed_new_password, memberid):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        sql_change_password = "UPDATE member_password SET hashed_password = %s WHERE member_id = %s"
        cursor.execute(sql_change_password, (hashed_new_password, memberid))
        conn.commit()

    finally:
        cursor.close()
        conn.close()

    return True

def delete_account(memberid):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql_delete_account = "DELETE FROM member WHERE member_id = %s"
        cursor.execute(sql_delete_account, (memberid,))
        conn.commit()

    finally:
        cursor.close()
        conn.close()

    return True


def delete_email(emailid):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql_delete_email = "DELETE FROM email WHERE email_id = %s"
        cursor.execute(sql_delete_email, (emailid,))
        conn.commit()

    finally:
        cursor.close()
        conn.close()

    return True
