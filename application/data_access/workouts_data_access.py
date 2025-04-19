import sys
import mysql
from flask import session

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

# <---Workout Videos --->
# optional filter parameters
# if none chosen will return all workout videos
def get_workout_video(goal=None, experience=None, time=None):
    """
    This function retrieves a list of workout videos from the database, optionally filtered by fitness goal,
    experience level, and time available. The function also formats each video link into an embeddable
    YouTube URL for display on the webpage.
    :param goal: str
    :param experience: str
    :param time: str
    :return: list of dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    # connect to database and create a cursor, used to execute SQL queries and fetch results

    # base query runs if no filters selected and returns all workout videos, and is appended later if filters are selected
    base_query = "SELECT video_name, video_link, fitness_goal, experience, time FROM v_workout_videos"
    filters = []

    # if filters selected on webpage, passed through function as parameters, added to the f string below (formatted to fit SQL query) and stored in filters list
    if goal:
        filters.append(f"fitness_goal = '{goal}'")
    if experience:
        filters.append(f"experience = '{experience}'")
    if time:
        filters.append(f"time = '{time}'")

    # if filters list not empty i.e. if any filters chosen
    if filters:
        conditions = " AND ".join(filters)
        base_query += " WHERE " + conditions
        # .join method takes the different elements in the filters list and makes a string using " AND " as the defined separator, and operator in SQL
        # spacing is important to make sure there are spaces between each condition
        # the new string made using the filters list is assigned to conditions
        # this is then appended to the base query, after " WHERE " (spacing again important) to use the SQL operator and apply conditions to the SQL query based on filters chosen on the webpage

    # run the final query and fetch the results
    cursor.execute(base_query)
    result = cursor.fetchall()
    # result is a list of tuples by default
    # each tuple represents a row from the database

    workout_video_list = []

    # for loop, for each tuple
    # first step is YouTube link taken from database, id extracted and inputted into correct string to embed YouTube videos, so that can be used in workout_videos.html
    # position 1 in each tuple (video_link, based on order SQL SELECT query) can be amended
    for item in result:
        video_link=item[1]
        video_id = get_youtube_video_id(video_link)
        embed_link = f"https://www.youtube.com/embed/{video_id}"

        # turn each tuple into a dictionary
        workout = {
            'video_name': item[0],
            'video_link': embed_link,
            'fitness_goal': item[2],
            'experience': item[3],
            'time': item[4]
        }
        workout_video_list.append(workout)
        # append the dictionary to the list
        #this is done for each tuple using the for loop

    return workout_video_list


def get_youtube_video_id(url):
    """
    This function takes a YouTube video URL and splits the string to separate the video id.
    The video id is needed to embed the YouTube video to a webpage.
    :param url: str
    :return: str
    """
    split_url = url.split('https://www.youtube.com/watch?v=')
    video_id = split_url[1]
    return video_id


def get_member_goal_id():
    """
    This function returns the goal_id of the user from the current session.
    goal_id can be null.
    :return: int or None
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    user_id = session.get('user_id')
    query = f"SELECT goal_id FROM member WHERE member_id = {user_id}"

    cursor.execute(query)
    result = cursor.fetchone()

    return result[0] if result else None


def get_member_fitness_goal():
    """
    This function returns the fitness goal of the user from the current session.
    Fitness goal can be null
    :return: str or None
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    goal_id = get_member_goal_id()

    if goal_id is None:
        return None

    else:
        query = f"SELECT fitness_goal FROM goal WHERE goal_id = {goal_id}"

        cursor.execute(query)
        result = cursor.fetchone()

        return result[0] if result else None


def get_member_experience_id():
    """
    This function returns the experience_id of the user from the current session.
    experience_id can be null.
    :return: int or None
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    user_id = session.get('user_id')
    query = f"SELECT experience_id FROM member WHERE member_id = {user_id}"

    cursor.execute(query)
    result = cursor.fetchone()

    return result[0] if result else None


def get_member_experience():
    """
    This function returns the experience level of the user from the current session.
    Experience level can be null
    :return: str or None
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    experience_id = get_member_experience_id()

    if experience_id is None:
        return None

    else:
        query = f"SELECT user_experience FROM experience WHERE experience_id = {experience_id}"

        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None


def get_exercises():
    """
    This function returns the exercises that relate to the fitness goal of the user in the current session.
    :return: list[str]
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    goal = get_member_goal_id()
    query = f"SELECT exercise_name FROM exercise WHERE goal_id = {goal}"

    cursor.execute(query)
    result = cursor.fetchall()

    # get just the exercise names from the tuples
    exercise_names = []
    for row in result:
        exercise_names.append(row[0])

    return exercise_names


def get_reps():
    """
    This function returns the reps for exercises based on the experience level of the user from the current session.
    :return: int or None
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    experience = get_member_experience_id()
    query = f"SELECT reps FROM experience WHERE experience_id = {experience}"

    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        return None


def get_sets():
    """
    This function returns the reps for exercises based on the experience level of the user from the current session.
    :return: int or None
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    experience = get_member_experience_id()
    query = f"SELECT sets FROM experience WHERE experience_id = {experience}"

    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        return None


def get_days_of_week():
    """
    This function returns the days of the week, Mon-Sun, stored as a list of strings.
    :return lst[str]:
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT day FROM day_of_week"

    cursor.execute(query)
    result = cursor.fetchall()

    # get a list of just names of days of the week from the tuple
    days_of_week = []
    for row in result:
        days_of_week.append(row[0])

    return days_of_week


def update_workout_progress(member_id, day_id, is_done):
    """
    This function updates or inserts into the 'workout_progress' table in the database to mark a day as done.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # check if a record for that user and day already exists
    check_query = "SELECT * FROM workout_progress WHERE member_id = %s AND day_id = %s"
    cursor.execute(check_query, (member_id, day_id))
    result = cursor.fetchone()
    # returns tuple (progress_id, member_id, day_id, is_done), and None if there is no entry for the user and day in the table

    # if the record exists, update it. otherwise, insert a new record
    if result:
        update_query = "UPDATE workout_progress SET is_done = %s WHERE member_id = %s AND day_id = %s"
        cursor.execute(update_query, (is_done, member_id, day_id))
    else:
        insert_query = "INSERT INTO workout_progress (member_id, day_id, is_done) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (member_id, day_id, is_done))

    # commit the changes to the database
    conn.commit()



def get_workout_progress(member_id):
    """
    This function checks the workout progress for a given member, stored in the database.
    :return: dict
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT day_id, is_done FROM workout_progress WHERE member_id = %s"

    # (member_id,) is a tuple - passed into the query in place of %s
    # unlike other functions above, member_id passed as parameter rather than included in function itself - just trying a different approach
    # member_id assigned in the route where this function is used, using session.get('user_id')
    cursor.execute(query, (member_id,))
    result = cursor.fetchall()

    # result is a list of tuples e.g. result = [(1, True), (2, False), (3, True)]
    # convert to dictionary, storing is_done value for each day for the member
    workout_progress = {}
    for item in result:
        # in the tuple, item[0] is the day_id and item[1] is True or False, depending if workout ticked as done that day
        workout_progress[item[0]] = item[1]

    return workout_progress



def main():
    return None

if __name__ == "__main__":
    main()