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


def main():
    return None


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
        SELECT m.member_id, m.first_name, m.last_name, e.email_address,
               m.date_of_birth, m.height, m.weight,
               g.fitness_goal, d.dietary_requirement, ex.user_experience,
               m.member_since
        FROM member m
        JOIN goal g ON m.goal_id = g.goal_id
        LEFT JOIN diet d ON m.diet_id = d.diet_id
        LEFT JOIN experience ex ON m.experience_id = ex.experience_id
        JOIN email e ON m.email_id = e.email_id
        WHERE m.member_id = %s
    """, (user_id,))

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        return {
            "id": row[0],
            "firstname": row[1],
            "lastname": row[2],
            "email": row[3],
            "dob": row[4],
            "height": row[5],
            "weight": row[6],
            "goal": row[7],
            "diet": row[8],
            "experience": row[9],
            "member_since": row[10]
        }
    else:
        return None


def get_all_goals():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT fitness_goal FROM goal")
    results = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return results


def get_all_experience_levels():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_experience FROM experience")
    results = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return results


def get_all_diets():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT dietary_requirement FROM diet")
    results = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return results


# def update_profile_info(user_id, dob, height, weight, goal_name, experience_name, diet_name):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#
#     # Get goal_id from goal name
#     cursor.execute("SELECT goal_id FROM goal WHERE fitness_goal = %s", (goal_name,))
#     goal_row = cursor.fetchone()
#     goal_id = goal_row[0] if goal_row else None
#
#     # Get experience_id from experience name
#     cursor.execute("SELECT experience_id FROM experience WHERE user_experience = %s", (experience_name,))
#     exp_row = cursor.fetchone()
#     experience_id = exp_row[0] if exp_row else None
#
#     # Get diet_id from diet name
#     cursor.execute("SELECT diet_id FROM diet WHERE dietary_requirement = %s", (diet_name,))
#     diet_row = cursor.fetchone()
#     diet_id = diet_row[0] if diet_row else None
#
#     # Only update if we found all relevant IDs
#     if goal_id and experience_id and diet_id:
#         cursor.execute("""
#             UPDATE member
#             SET date_of_birth = %s, height = %s, weight = %s,
#                 goal_id = %s, diet_id = %s
#             WHERE member_id = %s
#         """, (dob, height, weight, goal_id, diet_id, user_id))
#
#         # Optional: Save experience_id to another table if needed
#         # e.g., store it in a member_experience table or if your `member` table has that field
#
#         conn.commit()
#
#     cursor.close()
#     conn.close()


def update_height_weight(user_id, height, weight):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE member SET height = %s, weight = %s WHERE member_id = %s
    """, (height, weight, user_id))
    conn.commit()
    cursor.close()
    conn.close()


def update_fitness_preferences(user_id, goal_name, experience_name, diet_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Convert names to IDs
    cursor.execute("SELECT goal_id FROM goal WHERE fitness_goal = %s", (goal_name,))
    goal_id = cursor.fetchone()[0]

    cursor.execute("SELECT experience_id FROM experience WHERE user_experience = %s", (experience_name,))
    experience_id = cursor.fetchone()[0]

    cursor.execute("SELECT diet_id FROM diet WHERE dietary_requirement = %s", (diet_name,))
    diet_id = cursor.fetchone()[0]

    cursor.execute("""
        UPDATE member SET goal_id = %s, experience_id = %s, diet_id = %s
        WHERE member_id = %s
    """, (goal_id, experience_id, diet_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()


def update_dob(user_id, dob):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE member SET date_of_birth = %s WHERE member_id = %s", (dob, user_id))
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
