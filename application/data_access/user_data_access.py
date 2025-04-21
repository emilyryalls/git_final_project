import mysql.connector
import sys
import os
import json

from unicodedata import category

# Set MySQL password based on the system platform
if sys.platform == "win32":
    mysql_password = "password"
else:
    mysql_password = ""

def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.

    Returns:
        mydb (mysql.connector.connection.MySQLConnection): The database connection object.
    """
    # Connect to MySQL database with provided credentials
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password= mysql_password,
      database="rise_db")
    return mydb

#                                               <----- Login ------>
# Returns user details tuple or None
def get_details_by_email(useremail):
    """
    Fetches user details from the database based on the provided email address.

    Args:
        useremail (str): The email address of the user to look up.

    Returns:
        tuple: A tuple containing user details (hashed password, first name, email address, member id, email id).
        None: If no matching user is found.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # SQL query to get user details by email
        sql_get_password_name = "SELECT hashed_password, first_name, email_address, member_id, email_id FROM v_login_details WHERE email_address = %s"
        cursor.execute(sql_get_password_name, (useremail,))
        saved_tuple = cursor.fetchone()

    # We are not using except here because we are already handling that logic in the routes
    finally:             # Even if an error occurs
        cursor.close()   # Ensure the cursor is closed
        conn.close()     # Ensure the connection is closed
    return saved_tuple

#                                               <----- Add Member ------>

# Adds a new member to the database
def add_member(fname, lname, uemail, hpassword):
    """
    Adds a new member to the database, including checking if the email already exists.

    Args:
        fname (str): The first name of the member.
        lname (str): The last name of the member.
        uemail (str): The email address of the member.
        hpassword (str): The hashed password for the member.

    Returns:
        bool: True if the email already exists; otherwise, None.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if the email already exists in the database
        sql_check_email = "SELECT email_id FROM email WHERE email_address = %s"
        val_check = (uemail,)
        cursor.execute(sql_check_email, val_check)
        email_id = cursor.fetchone()

        if email_id:
            return True # Return true if email exist
        else:
            # Insert the new email into the email table
            sql_add_email = "INSERT INTO email (email_address) VALUES (%s)"
            val_email = (uemail,)
            cursor.execute(sql_add_email, val_email)   # Execute the query
            conn.commit()

            # Get new user email_id by querying the email table again
            cursor.execute(sql_check_email, (uemail,))
            new_email_id = cursor.fetchone()[0]

            # Insert the member's full name into the member table
            sql_add_full_name = "INSERT INTO member (first_name, last_name, email_id) VALUES (%s, %s, %s)"
            val_full_name = (fname, lname, new_email_id)
            cursor.execute(sql_add_full_name, val_full_name)

            # Get the new member_id
            sql_get_member_id = "SELECT member_id FROM member WHERE email_id = %s"
            val_member_id = (new_email_id,)
            cursor.execute(sql_get_member_id, val_member_id)
            new_member_id = cursor.fetchone()[0]

            # Insert the hashed password into the member_password table
            sql_add_password = "INSERT INTO member_password (hashed_password, member_id) VALUES (%s, %s)"
            val_password = (hpassword, new_member_id)
            cursor.execute(sql_add_password, val_password)
            conn.commit()

    finally:
        cursor.close()
        conn.close()


#####
def get_password_details_by_id(memberid):
    """
    Fetches the password details for a specific member based on their member ID.

    Args:
        memberid (int): The unique identifier of the member.

    Returns:
        tuple: A tuple containing the hashed password for the member.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # SQL query to retrieve password details based on member ID
        sql_get_password_id = "SELECT hashed_password FROM v_login_details WHERE member_id = %s"
        cursor.execute(sql_get_password_id, (memberid,))
        saved_tuple = cursor.fetchone()
        return saved_tuple

    finally:
        cursor.close()
        conn.close()

# Returns True if password updated successfully
def change_password(hashed_new_password, memberid):
    """
    Changes the password for a specific member in the database.

    Args:
        hashed_new_password (str): The new hashed password.
        memberid (int): The unique identifier of the member whose password is being changed.

    Returns:
        bool: True if the password is updated successfully.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # SQL query to update the password in the member_password table
        sql_change_password = "UPDATE member_password SET hashed_password = %s WHERE member_id = %s"
        cursor.execute(sql_change_password, (hashed_new_password, memberid))
        conn.commit()

    finally:
        cursor.close()
        conn.close()

    return True

def delete_account(memberid):
    """
    Deletes a member's account from the database based on their member ID.

    Args:
        memberid (int): The unique identifier of the member whose account is being deleted.

    Returns:
        bool: True if the account is successfully deleted.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # SQL query to delete the member's record from the member table
        sql_delete_account = "DELETE FROM member WHERE member_id = %s"
        cursor.execute(sql_delete_account, (memberid,))
        conn.commit()

    finally:
        cursor.close()
        conn.close()

    return True


def delete_email(emailid):
    """
    Deletes an email address from the database based on its email ID.

    Args:
        emailid (int): The unique identifier of the email to be deleted.

    Returns:
        bool: True if the email is successfully deleted.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # SQL query to delete the email from the email table
        sql_delete_email = "DELETE FROM email WHERE email_id = %s"
        cursor.execute(sql_delete_email, (emailid,))
        conn.commit()

    finally:
        cursor.close()
        conn.close()

    return True
