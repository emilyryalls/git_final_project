import sys
import mysql

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



def main():
    return None

if __name__ == "__main__":
    main()