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


# <---Workout Videos --->
def get_workout_video(goal=None, experience=None, time=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    if goal:
        sql_query_goal = "SELECT video_name, video_link, fitness_goal, experience, time FROM v_workout_videos WHERE goal = %s"
        cursor.execute(sql_query_goal, (goal,))

    elif experience:
        sql_query_experience = "SELECT video_name, video_link, fitness_goal, experience, time FROM v_workout_videos WHERE experience = %s"
        cursor.execute(sql_query_experience, (experience,))

    elif time:
        sql_query_time = "SELECT video_name, video_link, fitness_goal, experience, time FROM v_workout_videos WHERE time = %s"
        cursor.execute(sql_query_time, (time,))

    else:
        sql_query = "SELECT video_name, video_link, fitness_goal, experience, time FROM v_workout_videos"
        cursor.execute(sql_query)

    result = cursor.fetchall()
    workout_video_list = []
    for item in result:
        workout_video_list.append({'video_name': item[0], 'video_link': item[1], 'fitness_goal': item[2], 'experience': item[3], 'time': item[4]})

    return workout_video_list
