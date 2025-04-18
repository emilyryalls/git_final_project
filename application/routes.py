from re import match

from application import app
import mysql.connector
import os
from flask import render_template, request, redirect, url_for, flash, session
from application.data_access.blog_data_access import get_all_blogs,  get_blog_by_id
from application.data_access.data_access import add_member, get_details_by_email, get_password_details_by_id, change_password, delete_account, delete_email
from application.data_access.meal_plan_data_access import get_user_id, get_week_start_date, find_meal_plan_by_timestamp, get_db_connection
from application.data_access.profile_data_access import get_db_connection, get_user_by_id, get_all_diets, get_all_goals, get_all_experience_levels, update_dob, update_height_weight, update_fitness_preferences, update_profile_picture
# from application.data_access.user_data_access import get_user_by_id
from application.data_access.workouts_data_access import get_workout_video, get_exercises, get_sets, get_reps, \
    get_member_fitness_goal, get_member_experience, get_days_of_week, update_workout_progress, get_workout_progress
import re
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from urllib.parse import unquote



@app.route('/')
@app.route('/home')
def home():
    if not session.get('loggedIn'):
        return render_template('home.html', title='Home', loggedin=False)

    return render_template('home.html', title='Home', loggedin=True)


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


        if len(useremail) == 0 or len(userpassword) == 0 or len(userfirstname) == 0 or len(userlastname) == 0:
            error = 'Please supply all fields'
        elif add_member(userfirstname, userlastname, useremail, hashed_password):
            error_email_exist = 'Already part of the family! Log in instead 😊'
        elif not re.match(r"^[A-Za-zÀ-ÿ\s'-]+$", userfirstname) or not re.match(r"^[A-Za-zÀ-ÿ\s'-]+$", userlastname):
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
    error_invalid_credentials = ""

    if request.method == 'POST':
        useremail = request.form.get('userEmail')
        userpassword = request.form.get('userPassword')

        if len(useremail) == 0 or len(userpassword) == 0:
            error = 'Please supply all fields'
        else:
            saved_details = get_details_by_email(useremail)

            if saved_details: #if email exist
                stored_password = saved_details[0]
                session['email'] = saved_details[2]
                session['user'] = saved_details[1]
                session['user_id'] = saved_details[3]
                session['email_id'] = saved_details[4]
                session['loggedIn'] = True

                if check_password_hash(stored_password, userpassword):
                    return redirect(url_for('profile'))
                else:
                    error_invalid_credentials = 'Incorrect email or password. Please try again!'
            else:
                error_invalid_credentials = 'Incorrect email or password. Please try again!'
        return render_template('login.html', title='Sign In', message = error, message_invalid_credentials = error_invalid_credentials)
    return render_template('login.html', title='Sign In')


@app.route('/loggedout')
def logged_out():
    session.pop('email', None)
    session.pop('user', None)
    session.pop('user_id', None)
    session['loggedIn'] = False
    return redirect(url_for('home'))


@app.route('/reset', methods=['GET', 'POST'])
def reset_form():
    if not session.get('loggedIn'):
        return redirect(url_for('signin_form'))
    error_missing = ""
    error_different_password = ""
    error_invalid_password = ""

    if request.method == 'POST':
        current_password = request.form.get('currentPassword')
        new_password = request.form.get('newPassword')
        confirm_password = request.form.get('confirmPassword')
        member_id = session['user_id']

        if not member_id:
            return redirect(url_for('signin_form'))
        else:
            password_details = get_password_details_by_id(member_id)
            if password_details:
                stored_password = password_details[0]
                if len(current_password) == 0 or len(new_password) == 0 or len(confirm_password) == 0:
                    error_missing = 'Please supply all fields'
                else:
                    if check_password_hash(stored_password, current_password):
                        if new_password == confirm_password:
                            hashed_new_password = generate_password_hash(new_password)
                            change_password(hashed_new_password, member_id)
                            return render_template('login.html', title='Login')
                        else:
                            error_different_password = "Passwords do not match"
                    else:
                        error_invalid_password = "Incorrect Password, please try again"

    return render_template('reset.html', title='Reset', message_invalid_password=error_invalid_password, message_different_password=error_different_password, message_missing=error_missing)


@app.route('/delete', methods=['GET', 'POST'])
def delete_account_route():
    if not session.get('loggedIn'):
        return redirect(url_for('signin_form'))

    if request.method == 'POST':
       member_id = session.get('user_id')
       emailid = session.get('email_id')
       if not member_id:
           return redirect(url_for('signin_form'))
       else:
           delete_account(member_id)
           delete_email(emailid)
           session.clear()
           flash("Your account has been deleted. Your rise continues anytime.")
           return render_template('login.html', title='settings')

    return render_template('delete.html', title='Delete')



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



# --------------------------------------------------------------------------------------------------------------------- #
#                                               <---- Blogs ---->

# <-- all blogs and filter-->
@app.route('/blog_home', methods=['GET'])
def blogs():
    # Retrieve the 'category' parameter
    category = request.args.get('category')

    # If no category is selected, it fetches all blogs
    blog_database = get_all_blogs(category)

    # Pass the list of blogs to the 'blog_home' template
    return render_template('blog/blog_home.html', blog_list=blog_database)


# <--individual blog based on the blog ID-->
@app.route('/blog/<int:blog_id>', methods=['GET'])
def view_blog(blog_id):
    # Call the data access function to get the blog details
    blog = get_blog_by_id(blog_id)

    if blog is None:
        # If no blog is found, redirect to the blog home page
        return redirect(url_for('blogs'))

    # Render the template for the individual blog, passing the blog data
    return render_template('blog/view_blog.html', blog=blog)

# --------------------------------------------------------------------------------------------------------------------- #

#           <---- Meal planner ---->

# Config
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

@app.route('/meal_planner_form')
def meal_planner():
    if not get_user_id():
        return redirect(url_for('signin_form'))
    return redirect(url_for('meal_plan_dashboard'))


@app.route('/save_meal_plan', methods=['POST'])
def save_meal_plan():
    if not get_user_id():
        return redirect(url_for('signin_form'))

    user_id = get_user_id()
    monday = get_week_start_date()
    plan_name = f"Week of {monday.strftime('%d-%m-%y')}"

    week = {
        day: {
            'breakfast': request.form.get(f'{day}_breakfast', ''),
            'lunch': request.form.get(f'{day}_lunch', ''),
            'dinner': request.form.get(f'{day}_dinner', ''),
            'snacks': request.form.get(f'{day}_snacks', ''),
        } for day in DAYS
    }

    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    meal_plan = {
        'user_id': user_id,
        'name': plan_name,
        'description': request.form.get('meal_plan_description', ''),
        'week': week,
        'created_at': created_at
    }

    # Save meal plan to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO meal_plans (member_id, name, description, meals, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        meal_plan['user_id'],
        meal_plan['name'],
        meal_plan['description'],
        json.dumps(meal_plan['week']),  # Properly serializing the week as JSON
        meal_plan['created_at']
    ))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Meal Plan Saved!", "success")
    return redirect(url_for('meal_plan_dashboard', timestamp=created_at))

# Route to display the dashboard
@app.route('/meal_plan_dashboard', methods=['GET'])
def meal_plan_dashboard():
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for('signin_form'))

    monday = get_week_start_date()
    plan_name = f"Week of {monday.strftime('%d-%m-%y')}"

    # Load meal plans from the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM meal_plans WHERE member_id = %s ORDER BY created_at DESC", (user_id,))
    meal_plans = cursor.fetchall()
    cursor.close()
    conn.close()

    # Parse meals from JSON string to dict for each plan
    for plan in meal_plans:
        if isinstance(plan['meals'], str):
            try:
                plan['meals'] = json.loads(plan['meals'])
            except json.JSONDecodeError:
                plan['meals'] = {}

    current_meal_plan = meal_plans[0] if meal_plans else None
    timestamp = request.args.get('timestamp')

    selected_meal_plan = None
    if timestamp:
        selected_meal_plan = next((plan for plan in meal_plans if plan['created_at'] == timestamp), None)

    return render_template('meal_plan_dashboard.html',
                           meal_plans=meal_plans,
                           current_meal_plan=selected_meal_plan or current_meal_plan,
                           selected_meal_plan=selected_meal_plan,
                           plan_name=plan_name,
                           days=DAYS)

# <-- View a Specific Meal Plan -->
@app.route('/meal_plan_view/<timestamp>', methods=['GET'])
def view_meal_plan(timestamp):
    user_id = get_user_id()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM meal_plans WHERE member_id = %s AND created_at = %s", (user_id, timestamp))
    selected_meal_plan = cursor.fetchone()
    cursor.close()
    conn.close()

    if not selected_meal_plan:
        flash("Meal plan not found", "danger")
        return redirect(url_for('meal_plan_dashboard'))

    # Ensure meals is a dict (deserialize if it's a JSON string)
    if isinstance(selected_meal_plan['meals'], str):
        try:
            selected_meal_plan['meals'] = json.loads(selected_meal_plan['meals'])
        except json.JSONDecodeError:
            selected_meal_plan['meals'] = {}

    return render_template('meal_plan/view_meal_plan.html', selected_meal_plan=selected_meal_plan)

@app.route('/edit_meal_plan/<timestamp>', methods=['GET', 'POST'])
def edit_meal_plan(timestamp):
    timestamp = unquote(timestamp)  # <-- Add this line
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for('signin_form'))

    selected_meal_plan = find_meal_plan_by_timestamp(user_id, timestamp)
    if not selected_meal_plan:
        flash("Meal plan not found!", "danger")
        return redirect(url_for('meal_plan_dashboard'))

    if request.method == 'POST':
        description = request.form.get('meal_plan_description')
        plan_name = f"Week of {get_week_start_date().strftime('%d-%m-%y')}"

        meals = {
            day: {
                'breakfast': request.form.get(f'{day}_breakfast', ''),
                'lunch': request.form.get(f'{day}_lunch', ''),
                'dinner': request.form.get(f'{day}_dinner', ''),
                'snacks': request.form.get(f'{day}_snacks', ''),
            } for day in DAYS
        }

        # Update the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE meal_plans
            SET name = %s, description = %s, meals = %s
            WHERE member_id = %s AND created_at = %s
        """, (
            plan_name,
            description,
            json.dumps(meals),  # Properly serializing meals as JSON
            user_id,
            timestamp
        ))
        conn.commit()
        conn.close()

        flash("Meal Plan Updated!", "success")
        return redirect(url_for('meal_plan_dashboard', timestamp=timestamp))

    return render_template(
        'edit_meal_plan.html',
        selected_meal_plan=selected_meal_plan,
        days=DAYS
    )


@app.route('/clone_meal_plan/<timestamp>', methods=['GET', 'POST'])
def clone_meal_plan(timestamp):
    timestamp = unquote(timestamp)
    user_id = get_user_id()
    selected_meal_plan = find_meal_plan_by_timestamp(user_id, timestamp)

    if not selected_meal_plan:
        flash("Meal plan not found!", "danger")
        return redirect(url_for('meal_plan_dashboard'))

    if request.method == 'POST':
        monday = get_week_start_date()
        plan_name = f"Week of {monday.strftime('%d-%m-%y')}"
        description = request.form.get('meal_plan_description')
        timestamp_new = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        meals = {
            day: {
                'breakfast': request.form.get(f'{day}_breakfast', ''),
                'lunch': request.form.get(f'{day}_lunch', ''),
                'dinner': request.form.get(f'{day}_dinner', ''),
                'snacks': request.form.get(f'{day}_snacks', ''),
            } for day in DAYS
        }

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO meal_plans (member_id, name, description, created_at, meals)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            user_id,
            plan_name,
            description,
            timestamp_new,
            json.dumps(meals)
        ))
        conn.commit()
        conn.close()

        flash("Meal Plan Cloned!", "success")
        return redirect(url_for('meal_plan_dashboard', timestamp=timestamp_new))

    return render_template('edit_meal_plan.html', selected_meal_plan=selected_meal_plan, days=DAYS)


# -------------------------------------------------------------------------------------------------------------- #

# <---- Profile and profile settings ---->

# Route to display the user profile
@app.route("/profile", methods=["GET"])
def profile():
    if 'loggedIn' in session and session['loggedIn']:
        user_id = session.get('user_id')
        user = get_user_by_id(user_id)

        # Sync session with latest profile pic (useful for navbar display)
        session['profile_pic'] = user.get('profile_pic')

        # Check if redirected from settings with success message
        updated = request.args.get("updated")

        return render_template("profile.html", user=user, updated=updated)
    else:
        return redirect(url_for('signin_form'))  # Redirect to signin if not logged in

# Route to get profile settings page as well as to edit the profile details on it
@app.route("/profile/settings", methods=["GET", "POST"])
def profile_settings():
    # TEMP: Assume user_id = 1 for development/testing
    if 'loggedIn' not in session:
        return redirect(url_for('signin_form'))

    user_id = session['user_id']
    # user = get_user_by_id(user_id)

    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "account_info":
            dob_str = request.form.get("dob")
            if dob_str:
                from datetime import datetime, date
                dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
                today = date.today()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

                if age < 18:
                    flash("You must be at least 18 years old to update your profile.", "danger")
                    return redirect(url_for("profile_settings"))

                update_dob(user_id, dob)


        elif form_type == "body_metrics":
            height = request.form.get("height")
            weight = request.form.get("weight")
            update_height_weight(user_id, height.strip(), weight.strip())

        elif form_type == "preferences":
            goal = request.form.get("goal")
            experience = request.form.get("experience")
            diet = request.form.get("diet")
            update_fitness_preferences(user_id, goal, experience, diet)

        # # Refresh session user data
        # updated_user = get_user_by_id(user_id)
        # session['user'] = updated_user

        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile", updated=1))

    user = get_user_by_id(user_id)
    fitness_goals = get_all_goals()
    experiences = get_all_experience_levels()
    diets = get_all_diets()

    return render_template("profile_settings.html", user=user, fitness_goals=fitness_goals, experiences=experiences, diets=diets)


@app.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    if 'loggedIn' not in session or 'user_id' not in session:
        return redirect(url_for('signin_form'))

    if 'profile_pic' not in request.files:
        flash("No file part", "warning")
        return redirect(url_for('profile'))

    file = request.files['profile_pic']
    if file.filename == '':
        flash("No selected file", "warning")
        return redirect(url_for('profile'))

    if file:
        filename = secure_filename(file.filename)

        # ✅ Absolute path for saving the image
        upload_folder = os.path.join(app.root_path, 'static', 'images', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        full_path = os.path.join(upload_folder, filename)

        # ✅ Relative path for use in <img src=""> (convert backslashes to slashes)
        relative_path = os.path.join('images', 'uploads', filename).replace("\\", "/")

        file.save(full_path)
        print("SAVED TO:", full_path)
        print("Exists?", os.path.exists(full_path))

        update_profile_picture(session['user_id'], relative_path)
        session['profile_pic'] = relative_path
        flash("Profile picture updated successfully!", "success")
        print("SAVED PATH (relative):", relative_path)

    return redirect(url_for('profile'))


# Workout Videos
# return all workout videos
@app.route('/workouts', methods=['GET'])
def view_workout_videos():
    # request is a special object in flask that gives you access to data sent by the client (browser)
    # request.args is a dictionary-like object that holds all of the querey paramteres from the URL
    # example - .get('goal') retrieves the value of the goal parameter from the URL
    # goal is a parameter defined in data_access.py
    goal = request.args.get('goal')
    experience = request.args.get('experience')
    time = request.args.get('time')
    workout_video = get_workout_video(goal, experience, time)
    return render_template('workout_videos.html', video=workout_video, title='Workout Videos')


# Workout Plan
@app.route('/my_workouts', methods=['GET'])
def view_workout_plan():

    # if user not logged in don't run the rest of the code
    if not session.get("user_id"):
        return redirect("/login")

    fitness_goal = get_member_fitness_goal()
    member_experience = get_member_experience()

    # return different error messages if user hasn't picked a fitness goal and/or experience level. on the webpage they will be told to pick both to access their personalised workout plan. if statements used in member_workouts.html to return these error messages if goal and/or experience have no value

    if fitness_goal is None and member_experience is None:
        return render_template('member_workouts.html', fitness_goal=None, experience = None, error_message ="You need to select both your fitness goal and experience level to access your workout plan")

    if fitness_goal is None:
        return render_template('member_workouts.html', fitness_goal=None, experience= member_experience, error_message="You need to select a fitness goal to access your workout plan")

    if member_experience is None:
        return render_template('member_workouts.html', fitness_goal = fitness_goal, experience = None, error_message="You need to select your experience level to access your workout plan")


    exercise_plan = get_exercises()
    sets = get_sets()
    reps = get_reps()
    days = get_days_of_week()
    workout_progress = get_workout_progress(session.get('user_id')) # session.get('user_id') used directly in the route and passed through as a parameter to get member_id
    workout_video = get_workout_video(fitness_goal, member_experience)
    # getting workouts that fit the member's fitness goal and experience level

    return render_template('member_workouts.html', exercises = exercise_plan, sets = sets, reps = reps, fitness_goal = fitness_goal, experience = member_experience, days = days, workout_progress = workout_progress, video=workout_video)


@app.route('/mark_workout_done', methods=['POST'])
def mark_workout_done():
    member_id = request.form.get('member_id')
    # another way of getting member_id - it is passed through as a hidden value in the html form in member_workouts.html

    # loop through day_ids 1 to 6 (7 is not inclusive) - Mon-Sat. Not Sunday as it is hard coded as a rest day in member_workouts.html
    for day_id in range(1, 7):
        checkbox_name = f'is_done_{day_id}' #generates strings is_done_1, is_done_2 etc. to is_done_6. they correspond to each checkbox in the html form, defined in member_workouts.html
        is_done = checkbox_name in request.form
        # request.form is a special object in flask that contains all the form data sent via POST method
        # this checks if the checkbox for the current day_id exists in the request.form
        # in html, checkboxes only appear in form data if they are checked
        # if the box is checked in the form, is_done is True
        # if the box is unchecked, is_done is False, as it doesn't exist in request.form

        # update the workout_progress table in the database
        # this function checks if an entry already exists for the day and user, and updates if it does, or inserts a new entry to the table if it doesn't
        # this is included in the for loop, so this is done for every day_id, either True or False is given
        update_workout_progress(member_id, day_id, is_done)

    # stay on the /my_workouts page after checking a box to mark a day as complete
    return redirect('/my_workouts')


