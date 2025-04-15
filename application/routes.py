from application import app
from flask import render_template, request, redirect, url_for, flash, session
from application.data_access.blog_data_access import get_all_blogs,  get_blog_by_id
from application.data_access.user_data_access import update_profile_info
from application.data_access.data_access import add_member, get_details_by_email
from application.data_access.workout_data_access import get_workout_video
from application.data_access.meal_plan_data_access import save_plan_to_file, load_latest_plan, get_user_id, get_user_plan_files, generate_plan_filename, get_week_start_date, find_meal_plan_by_timestamp
import os
import re
import json
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
@app.route('/home')
def home():
    session['loggedIn'] = False

    return render_template('home.html', title='Home')


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
            error_email_exist = 'Already part of the family! Log in instead 😊'
        elif not re.match(r"^[A-Za-zÀ-ÿ\s'-]+$", userfirstname) or not re.match(r"^[A-Za-zÀ-ÿ\s'-]+$", userlastname):
            error = 'First name and last name can only contain letters, spaces, apostrophes (\'), and hyphens (-).'
        else:
            add_member(userfirstname, userlastname, useremail, hashed_password)
            return render_template('signedup.html')
    return render_template('membership.html', title='Sign Up', message = error, message_email_exist = error_email_exist)


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
                session['loggedIn'] = True

                if check_password_hash(stored_password, userpassword):
                    return redirect(url_for('profile'))
                else:
                    error_invalid_credentials = 'Incorrect email or password. Please try again!'
            else:
                error_invalid_credentials = 'Incorrect email or password. Please try again!'
        return render_template('login.html', title='Sign In', message = error, message_invalid_credentials = error_invalid_credentials)
    return render_template('login.html', title='Sign In')

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

#                                           <---- Meal planner ---->

# Config
USER_MEAL_PLANS_DIR = os.path.join(os.path.dirname(__file__), 'user_meal_plans')
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MAX_MEAL_PLANS = 6

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

    created_at = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    meal_plan = {
        'user_id': user_id,
        'name': plan_name,
        'description': request.form.get('meal_plan_description', ''),
        'week': week,
        'created_at': created_at
    }

    save_plan_to_file(user_id, meal_plan)
    flash("Meal Plan Saved!", "success")
    return redirect(url_for('meal_plan_dashboard', timestamp=created_at))

# Route to display the dashboard
@app.route('/meal_plan_dashboard', methods=['GET'])
def meal_plan_dashboard():
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for('signin_form'))

    # Calculate default plan name
    monday = get_week_start_date()
    plan_name = f"Week of {monday.strftime('%d-%m-%y')}"

    # Load plans (newest first)
    user_files = get_user_plan_files(user_id)
    meal_plans = []
    for filename in sorted(user_files, reverse=True):
        with open(os.path.join(USER_MEAL_PLANS_DIR, filename), 'r') as f:
            data = json.load(f)
            meal_plans.append({
                'name': data.get('name'),
                'created_at': data.get('created_at'),
                'timestamp': data.get('created_at'),
                'description': data.get('description'),
                'meals': data.get('meals', data.get('week'))
            })

    timestamp = request.args.get('timestamp')
    selected_meal_plan = next((plan for plan in meal_plans if plan['timestamp'] == timestamp), None)

    print(f"Selected Meal Plan: {selected_meal_plan}")  # Add this
    return render_template('meal_plan_dashboard.html',
                           meal_plans=meal_plans,
                           selected_meal_plan=selected_meal_plan,
                           plan_name=plan_name,
                           days=DAYS)


# <-- View a Specific Meal Plan -->
@app.route('/meal_plan_view/<timestamp>', methods=['GET'])
def view_meal_plan(timestamp):
    # Load the meal plan corresponding to the timestamp
    user_id = get_user_id()
    user_files = get_user_plan_files(user_id)

    # Find the meal plan with the matching timestamp
    selected_meal_plan = None
    for filename in user_files:
        with open(os.path.join(USER_MEAL_PLANS_DIR, filename), 'r') as f:
            data = json.load(f)
            if data.get('created_at') == timestamp:
                selected_meal_plan = data
                break

    if selected_meal_plan is None:
        flash("Meal plan not found", "danger")
        return redirect(url_for('meal_plan_dashboard'))

    # Render the view for the selected meal plan
    return render_template('meal_plan/view_meal_plan.html', selected_meal_plan=selected_meal_plan)


def load_user_meal_plans(user_id):
    """Load meal plans for a user."""
    user_files = get_user_plan_files(user_id)
    meal_plans = []

    for filename in reversed(user_files[:4]):  # Limit to the 4 most recent plans
        try:
            with open(os.path.join(USER_MEAL_PLANS_DIR, filename), 'r') as f:
                data = json.load(f)
                meal_plans.append({
                    'name': data.get('name'),
                    'created_at': data.get('created_at'),
                    'timestamp': data.get('created_at'),  # For URL linking
                    'filename': filename
                })
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    return meal_plans


@app.route('/edit_meal_plan/<timestamp>', methods=['GET', 'POST'])
def edit_meal_plan(timestamp):
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for('signin_form'))

    selected_meal_plan = find_meal_plan_by_timestamp(user_id, timestamp)
    if not selected_meal_plan:
        flash("Meal plan not found!", "danger")
        return redirect(url_for('meal_plan_dashboard'))

    if request.method == 'POST':
        # Preserve original timestamp and update content
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

        updated_plan = {
            'user_id': user_id,
            'name': plan_name,
            'description': description,
            'created_at': selected_meal_plan['created_at'],  # maintain original
            'meals': meals
        }

        filename = f"{user_id}_meal_plan_{selected_meal_plan['created_at']}.json"
        with open(os.path.join(USER_MEAL_PLANS_DIR, filename), 'w') as f:
            json.dump(updated_plan, f)

        flash("Meal Plan Updated!", "success")
        return redirect(url_for('meal_plan_dashboard', timestamp=selected_meal_plan['created_at']))

    return render_template(
        'edit_meal_plan.html',
        selected_meal_plan=selected_meal_plan,
        days=DAYS
    )


@app.route('/clone_meal_plan/<timestamp>', methods=['GET', 'POST'])
def clone_meal_plan(timestamp):
    user_id = get_user_id()
    selected_meal_plan = find_meal_plan_by_timestamp(user_id, timestamp)

    if not selected_meal_plan:
        flash("Meal plan not found!", "danger")
        return redirect(url_for('meal_plan_dashboard'))

    if request.method == 'POST':
        monday = get_week_start_date()
        plan_name = f"Week of {monday.strftime('%d-%m-%y')}"
        description = request.form.get('meal_plan_description')
        timestamp_new = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        meals = {
            day: {
                'breakfast': request.form.get(f'{day}_breakfast', ''),
                'lunch': request.form.get(f'{day}_lunch', ''),
                'dinner': request.form.get(f'{day}_dinner', ''),
                'snacks': request.form.get(f'{day}_snacks', ''),
            } for day in DAYS
        }

        cloned_plan = {
            'user_id': user_id,
            'name': plan_name,
            'description': description,
            'created_at': timestamp_new,
            'meals': meals
        }

        filename = f"{user_id}_meal_plan_{timestamp_new}.json"
        with open(os.path.join(USER_MEAL_PLANS_DIR, filename), 'w') as f:
            json.dump(cloned_plan, f)

        flash("Meal Plan Cloned!", "success")
        return redirect(url_for('meal_plan_dashboard', timestamp=timestamp_new))

    return render_template('edit_meal_plan.html', selected_meal_plan=selected_meal_plan, days=DAYS)




# -------------------------------------------------------------------------------------------------------------- #

# Fitness goals list - to be removed once we have database
fitness_goals = [
    "Build Muscle",
    "Improve Stamina",
    "Lose Weight",
    "Tone Up"
]

# Route to display the user profile
@app.route("/profile", methods=["GET"])
def profile():
    if 'loggedIn' in session and session['loggedIn']:
        user = session['user']

    # TEMP: Assume user_id = 1 for development/testing
    # user_id = 1
    # user = get_user_by_id(user_id)
        return render_template("profile.html", user=user)
    else:
        return redirect(url_for('signin_form'))  # Redirect to signin if not logged in

# Route to edit profile details on settings page
@app.route("/profile/settings", methods=["GET", "POST"])
def update_profile():
    # TEMP: Assume user_id = 1 for development/testing
    # user_id = 1
    # user = get_user_by_id(user_id)
    if 'loggedIn' not in session:
        return redirect(url_for('signin_form'))
    else:
        user = session['user']
        user_id = session['user_id']

        if request.method == "POST":
            dob = request.form.get("dob")
            height = request.form.get("height")
            weight = request.form.get("weight")
            goal = request.form.get("goal")

            # update_profile_info(dob, height, weight, goal)
            update_profile_info(user_id, dob, height, weight, goal)
            flash("Profile updated successfully!")
            return redirect(url_for("profile"))

        return render_template("profile_settings.html", user=user, fitness_goals=fitness_goals)


# return all workout videos
@app.route('/workouts', methods=['GET'])
def view_workout_videos():
    workout_video = get_workout_video()
    return render_template('workout_videos.html', video=workout_video, title='Workout Videos')
