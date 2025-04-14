from application import app
import mysql.connector
from flask import render_template, request, redirect, url_for, flash, session
from application.blog_data_access import get_db_connection, add_member, get_password_by_email, get_all_blogs, get_blog_by_id, get_workout_video
import os
import re
import json
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

from application.profile_data_access import get_db_connection, get_user_by_id, get_all_diets, get_all_goals, get_all_experience_levels, update_dob, update_height_weight, update_fitness_preferences



@app.route('/')
@app.route('/home')
def home():
    # session['SignIn'] = False
    return render_template('home.html', title='Home')

# <---- Sign up / membership ---->
@app.route('/membership', methods=['GET'])
def signup_form():
    return render_template('membership.html', title='Membership')


@app.route('/signup', methods=['GET', 'POST'])
def signup_submit():
    error = ""
    error_email_exist = ""
    if request.method == 'POST':
        userfirstname = request.form.get('userName')
        userlastname = request.form.get('userLastname')
        useremail = request.form.get('userEmail')
        userpassword = request.form.get('userPassword')
        hashed_password = generate_password_hash(userpassword)
        #print('received')

        if len(useremail) == 0 or len(userpassword) == 0 or len(userfirstname) == 0 or len(userlastname) == 0:
            error = 'Please supply all fields'
        elif add_member(userfirstname, userlastname, useremail, hashed_password):
            error_email_exist = 'This email address is already part of the family! Please log in to continue.'
        elif not re.match("^[A-Za-zÀ-ÿ\s'-]+$", userfirstname) or not re.match("^[A-Za-zÀ-ÿ\s'-]+$", userlastname):
            error = 'First name and last name can only contain letters, spaces, apostrophes (\'), and hyphens (-).'
        else:
            add_member(userfirstname, userlastname, useremail, hashed_password)
            return render_template('signedup.html')
    return render_template('membership.html', title='Sign Up', message = error, message_email_exist = error_email_exist)


# <---- Login.logout ---->
@app.route('/login', methods=['GET', 'POST'])
def signin_form():
    return render_template('login.html', title='Login')


@app.route('/signin', methods=['GET', 'POST'])
def signin_submit():
    error = ""
    error_invalid_password = ""
    error_email_exist = ""

    if request.method == 'POST':
        useremail = request.form.get('userEmail')
        userpassword = request.form.get('userPassword')

        if len(useremail) == 0 or len(userpassword) == 0:
            error = 'Please supply all fields'
        else:
            saved_password = get_password_by_email(useremail)

            if saved_password:
                stored_password = saved_password[0]
                if check_password_hash(stored_password, userpassword):
                    return render_template('home.html')
                else:
                    error_invalid_password = 'Incorrect password, please try again!'
            else:
                error_email_exist = 'Email not found. Please sign up or try again'
        return render_template('login.html', title='Sign In', message = error, message_email_exist = error_email_exist, message_invalid_password = error_invalid_password)
    return render_template('login.html', title='Sign In')


# <---- Blogs ---->
# <-- all blogs and filter-->
@app.route('/blog_home', methods=['GET'])
def blogs():
    # Retrieve the 'category' parameter
    category = request.args.get('category')

    # If no category is selected, it fetches all blogs
    blog_database = get_all_blogs(category)

    # Pass the list of blogs to the 'blog_home' template
    return render_template('blog_home.html', blog_list=blog_database)


# <--individual blog based on the blog ID-->
@app.route('/blog/<int:blog_id>', methods=['GET'])
def view_blog(blog_id):
    # Call the data access function to get the blog details
    blog = get_blog_by_id(blog_id)

    if blog is None:
        # If no blog is found, redirect to the blog home page
        return redirect(url_for('blogs'))

    # Render the template for the individual blog, passing the blog data
    return render_template('view_blog.html', blog=blog)


# <--Newsletter subscription-->
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')

    if not email:
        flash("Please enter a valid email address.")
        return redirect(url_for('blogs'))  # Redirect back to blogs page

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if the email already exists
        cursor.execute("SELECT email_id FROM email WHERE email_address = %s", (email,))
        existing = cursor.fetchone()

        if existing:
            email_id = existing[0]
        else:
            # Add to email table
            cursor.execute("INSERT INTO email (email_address) VALUES (%s)", (email,))
            conn.commit()
            email_id = cursor.lastrowid

        # Insert into newsletter table (if not already subscribed)
        cursor.execute("SELECT * FROM newsletter WHERE email_id = %s", (email_id,))
        already_subscribed = cursor.fetchone()

        if not already_subscribed:
            cursor.execute("INSERT INTO newsletter (email_id) VALUES (%s)", (email_id,))
            conn.commit()

        flash("🎉 Thanks for subscribing!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash("❌ Something went wrong. Please try again.")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('blogs'))  # Go back to the blog page after subscribing


# <---- Meal planner ---->

# Directory to store user meal plans
USER_MEAL_PLANS_DIR = os.path.join(os.path.dirname(__file__), 'user_meal_plans')
# List of days for the meal planner
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


# <--display the meal planner form-->
@app.route('/meal_planner_form', methods=['GET'])
def meal_planner():
    # Get today's date
    today = datetime.now()

    # Calculate the Monday of the current week
    monday = today - timedelta(days=today.weekday())

    # Format the date as string in 'DD-MM-YY' format (for example: '06-03-23')
    plan_name = monday.strftime('%d-%m-%y')

    # Pass the 'plan_name' (week's start date) to the template along with 'days'
    return render_template('meal_planner_form.html', days=DAYS, plan_name=plan_name)


# <--saving the meal plan-->
@app.route('/save_meal_plan', methods=['POST'])
def save_meal_plan():
    # Get the meal plan name from the form
    plan_name = request.form.get('plan_name')

    # Initialize an empty dictionary to store meals for each day of the week
    week = {}
    for day in DAYS:
        # For each day, get the meals (breakfast, lunch, dinner, snacks) from the form
        week[day] = {
            'breakfast': request.form.get(f'{day}_breakfast', ''),
            'lunch': request.form.get(f'{day}_lunch', ''),
            'dinner': request.form.get(f'{day}_dinner', ''),
            'snacks': request.form.get(f'{day}_snacks', ''),
        }

    # Create the complete meal plan dictionary with the user ID, plan name, and weekly meals
    meal_plan = {
        'user_id': 'user123',  # set user id for testing change to current_user.id once database is created
        'name': plan_name,
        'week': week
    }

    # Save the meal plan as a JSON file (user-specific)
    user_meal_plan_file = os.path.join(USER_MEAL_PLANS_DIR, 'user123_meal_plan.json')
    try:
        with open(user_meal_plan_file, 'w') as f:
        # Write the meal plan data to the JSON file with indentation for readability
            json.dump(meal_plan, f, indent=4)
    except Exception as e:
        return render_template('error.html', message=f"Failed to save meal plan: {e}")

    return redirect(url_for('view_meal_plan'))

# <--view the saved meal plan-->
@app.route('/view_meal_plan', methods=['GET'])
def view_meal_plan():
    # Define the path to the saved user meal plan JSON file
    user_meal_plan_file = os.path.join(USER_MEAL_PLANS_DIR, 'user123_meal_plan.json')
    # user_meal_plan_file = os.path.join(USER_MEAL_PLANS_DIR, f'user_{current_user.id}_meal_plan.json') <--Use this once we have user table set up -->

    # Check if the meal plan file exists
    if not os.path.exists(user_meal_plan_file):
        # If it doesn't, render an error page
        return render_template('error.html', message="No meal plan found.")

    # Open and read the meal plan from the JSON file
    with open(user_meal_plan_file, 'r') as f:
        meal_plan = json.load(f)


    # Ensure the plan name exists and is properly extracted
    plan_name = meal_plan.get('name', 'NONE')  # If no plan name is found, it will default to 'NONE'

    # Render the 'view_meal_plan' template and pass the meal plan data
    return render_template('view_meal_plan.html', meal_plan=meal_plan, plan_name=plan_name)


# <---- Profile and profile settings ---->

# Route to display the user profile
@app.route("/profile", methods=["GET"])
def profile():
    # TEMP: Assume user_id = 1 for development/testing
    user_id = 1
    user = get_user_by_id(user_id)
    return render_template("profile.html", user=user)


# Route to get profile settings page as well as to edit the profile details on it
@app.route("/profile/settings", methods=["GET", "POST"])
def profile_settings():
    user_id = 1  # TEMP: until login system is in place
    user = get_user_by_id(user_id)

    fitness_goals = get_all_goals()
    experiences = get_all_experience_levels()
    diets = get_all_diets()

    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "account_info":
            # Just for future expansion (currently not updating these fields)
            dob = request.form.get("dob")
            update_dob(user_id, dob)  # Optional: make this function

        elif form_type == "body_metrics":
            height = request.form.get("height")
            weight = request.form.get("weight")
            update_height_weight(user_id, height, weight)

        elif form_type == "preferences":
            goal = request.form.get("goal")
            experience = request.form.get("experience")
            diet = request.form.get("diet")
            update_fitness_preferences(user_id, goal, experience, diet)

        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile_settings"))

    return render_template(
        "profile_settings.html",
        user=user,
        fitness_goals=fitness_goals,
        experiences=experiences,
        diets=diets
    )

# <---- Workout videos ---->
# return all workout videos
@app.route('/workouts', methods=['GET'])
def view_workout_videos():
    workout_video = get_workout_video()
    return render_template('workout_videos.html', video=workout_video, title='Workout Videos')
