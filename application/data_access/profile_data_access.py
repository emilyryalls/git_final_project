import mysql.connector
import sys
from datetime import datetime


if sys.platform == "win32":
    mysql_password = "password"
else:
    mysql_password = ""

def main():
    return None

def get_db_connection():
    """
    Establish and return a connection to the MySQL database.
    :return: mysql.connector.connection.MySQLConnection: A connection object to the rise_db database.
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=mysql_password,
        database="rise_db"
    )
    return mydb


def get_user_by_id(user_id):
    """
    Retrieve a user's complete profile information by their member ID.
    :param user_id: The member's ID (int).
    :return: dict or None: A dictionary containing user data if found, otherwise None.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.member_id,
               m.first_name,
               m.last_name,
               e.email_address,
               m.date_of_birth,
               m.height,
               m.weight,
               g.fitness_goal,
               d.dietary_requirement,
               ex.user_experience,
               m.member_since,
               m.profile_pic
        FROM member m
        LEFT JOIN goal g ON m.goal_id = g.goal_id
        LEFT JOIN diet d ON m.diet_id = d.diet_id
        LEFT JOIN experience ex ON m.experience_id = ex.experience_id
        LEFT JOIN email e ON m.email_id = e.email_id
        WHERE m.member_id = %s
    """, (user_id,))

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        dob = row[4]
        member_since = row[10]

        # Convert strings to datetime if they aren't already
        if isinstance(dob, str):
            try:
                dob = datetime.strptime(dob, "%Y-%m-%d")
            except:
                dob = None

        if isinstance(member_since, str):
            try:
                member_since = datetime.strptime(member_since, "%Y-%m-%d")
            except:
                member_since = None

        return {
            "id": row[0],
            "firstname": row[1],
            "lastname": row[2],
            "email": row[3],
            "dob": dob,
            "height": float(row[5]) if row[5] is not None else None,
            "weight": float(row[6]) if row[6] is not None else None,
            "goal": row[7],
            "diet": row[8],
            "experience": row[9],
            "member_since": member_since,
            "profile_pic": row[11] or 'images/profile_img/default_profile.png'
        }
    else:
        return None


def get_all_goals():
    """
    Retrieve all fitness goals from the database.
    :return: list: A list of all available fitness goal names.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT fitness_goal FROM goal")
    results = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return results


def get_all_experience_levels():
    """
    Retrieve all user experience levels from the database.
    :return: list: A list of experience level names.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_experience FROM experience")
    results = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return results


def get_all_diets():
    """
    Retrieve all dietary preferences from the database.
    :return: list: A list of dietary requirement options.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT dietary_requirement FROM diet")
    results = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return results


def update_height_weight(user_id, height, weight):
    """
     Update the height and/or weight for a specific user.
    :param user_id: (int): The member's ID.
    :param height: (float or str): The new height in cm.
    :param weight: (float or str): The new weight in kg.
    :return:
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    if height != "":
        cursor.execute("UPDATE member SET height = %s WHERE member_id = %s", (height, user_id))
    if weight != "":
        cursor.execute("UPDATE member SET weight = %s WHERE member_id = %s", (weight, user_id))

    conn.commit()
    cursor.close()
    conn.close()


def update_fitness_preferences(user_id, goal_name, experience_name, diet_name):
    """
    Update a user's fitness preferences. Allows partial updates — users may choose to update one, two, or all fields.
    :param user_id: (int): The member's ID.
    :param goal_name: (str): Selected fitness goal name (can be empty).
    :param experience_name: (str): Selected experience level name (can be empty).
    :param diet_name: (str): Selected dietary requirement name (can be empty).
    :return:
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    if goal_name and goal_name.strip():
        cursor.execute("SELECT goal_id FROM goal WHERE fitness_goal = %s", (goal_name,))
        result = cursor.fetchone()
        if result:
            goal_id = result[0]
            cursor.execute("UPDATE member SET goal_id = %s WHERE member_id = %s", (goal_id, user_id))

    if experience_name and experience_name.strip():
        cursor.execute("SELECT experience_id FROM experience WHERE user_experience = %s", (experience_name,))
        result = cursor.fetchone()
        if result:
            experience_id = result[0]
            cursor.execute("UPDATE member SET experience_id = %s WHERE member_id = %s", (experience_id, user_id))

    if diet_name and diet_name.strip():
        cursor.execute("SELECT diet_id FROM diet WHERE dietary_requirement = %s", (diet_name,))
        result = cursor.fetchone()
        if result:
            diet_id = result[0]
            cursor.execute("UPDATE member SET diet_id = %s WHERE member_id = %s", (diet_id, user_id))

    conn.commit()
    cursor.close()
    conn.close()


def update_dob(user_id, dob):
    """
    Update the date of birth for a given user.
    :param user_id: (int): The member's ID.
    :param dob: (str or datetime): The new date of birth in YYYY-MM-DD format.
    :return:
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE member SET date_of_birth = %s WHERE member_id = %s", (dob, user_id))
    conn.commit()
    cursor.close()
    conn.close()


def update_profile_picture(user_id, profile_pic_path):
    """
    Update the profile picture path for a given user.
    :param user_id: (int): The member's ID.
    :param profile_pic_path: (str): The path to the profile image file.
    :return:
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE member SET profile_pic = %s WHERE member_id = %s", (profile_pic_path, user_id))
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
