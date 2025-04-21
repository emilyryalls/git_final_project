import mysql.connector
import sys
import os
import json

from unicodedata import category

# Handle MySQL password based on platform
if sys.platform == "win32":
    mysql_password = "password"
else:
    mysql_password = ""

def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: The database connection object.
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=mysql_password,
        database="rise_db"
    )
    return mydb

# ---------------------------- <----- Login -----> ----------------------------

def get_details_by_email(useremail):
    """
    Retrieves login details (hashed password, name, email, IDs) from the login view using the email address.

    Args:
        useremail (str): The user's email address.

    Returns:
        tuple: A tuple containing hashed_password, first_name, email_address, member_id, and email_id.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_get_password_name = "SELECT hashed_password, first_name, email_address, member_id, email_id FROM v_login_details WHERE email_address = %s"
    cursor.execute(sql_get_password_name, (useremail,))
    saved_tuple = cursor.fetchone()

    conn.commit()
    return saved_tuple

# ---------------------------- <----- Add Member -----> ----------------------------

def add_member(fname, lname, uemail, hpassword):
    """
    Adds a new member to the database if their email doesn't already exist.

    Args:
        fname (str): First name of the user.
        lname (str): Last name of the user.
        uemail (str): Email address of the user.
        hpassword (str): Hashed password.

    Returns:
        bool: True if the email already exists, otherwise None.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if email already exists
    sql_check_email = "SELECT email_id FROM email WHERE email_address = %s"
    val_check = (uemail,)
    cursor.execute(sql_check_email, val_check)
    email_id = cursor.fetchone()

    if email_id:
        return True  # Return true if email exists
    else:
        # Insert the new email
        sql_add_email = "INSERT INTO email (email_address) VALUES (%s)"
        val_email = (uemail,)
        cursor.execute(sql_add_email, val_email)
        conn.commit()

        # Retrieve the new email ID
        cursor.execute(sql_check_email, (uemail,))
        new_email_id = cursor.fetchone()[0]

        # Insert full name into member table
        sql_add_full_name = "INSERT INTO member (first_name, last_name, email_id) VALUES (%s, %s, %s)"
        val_full_name = (fname, lname, new_email_id)
        cursor.execute(sql_add_full_name, val_full_name)

        # Get new member_id
        sql_get_member_id = "SELECT member_id FROM member WHERE email_id = %s"
        val_member_id = (new_email_id,)
        cursor.execute(sql_get_member_id, val_member_id)
        new_member_id = cursor.fetchone()[0]

        # Insert password for the new member
        sql_add_password = "INSERT INTO member_password (hashed_password, member_id) VALUES (%s, %s)"
        val_password = (hpassword, new_member_id)
        cursor.execute(sql_add_password, val_password)
        conn.commit()

def get_password_details_by_id(memberid):
    """
    Retrieves the hashed password for a member by their member ID.

    Args:
        memberid (int): The ID of the member.

    Returns:
        tuple: A tuple containing the hashed password.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_get_password_id = "SELECT hashed_password FROM v_login_details WHERE member_id = %s"
    cursor.execute(sql_get_password_id, (memberid,))
    saved_tuple = cursor.fetchone()

    conn.commit()
    return saved_tuple

def change_password(hashed_new_password, memberid):
    """
    Updates the password for a member in the database.

    Args:
        hashed_new_password (str): The new hashed password.
        memberid (int): The ID of the member.

    Returns:
        bool: True if the update was successful.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_change_password = "UPDATE member_password SET hashed_password = %s WHERE member_id = %s"
    cursor.execute(sql_change_password, (hashed_new_password, memberid))

    conn.commit()
    return True

def delete_account(memberid):
    """
    Deletes a member account from the database.

    Args:
        memberid (int): The ID of the member to delete.

    Returns:
        bool: True if deletion was successful.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_delete_account = "DELETE FROM member WHERE member_id = %s"
    cursor.execute(sql_delete_account, (memberid,))

    conn.commit()
    return True

def delete_email(emailid):
    """
    Deletes an email entry from the database.

    Args:
        emailid (int): The ID of the email to delete.

    Returns:
        bool: True if deletion was successful.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_delete_email = "DELETE FROM email WHERE email_id = %s"
    cursor.execute(sql_delete_email, (emailid,))

    conn.commit()
    return True