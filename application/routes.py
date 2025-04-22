from application import app
import mysql.connector
import os
import random
from flask import render_template, request, redirect, url_for, flash, session
from application.data_access.blog_data_access import get_all_blogs,  get_blog_by_id
from application.data_access.user_data_access import add_member, get_details_by_email, get_password_details_by_id, change_password, delete_account, delete_email
from application.data_access.meal_plan_data_access import get_user_id, get_week_start_date, find_meal_plan_by_timestamp, get_db_connection
from application.data_access.profile_data_access import get_db_connection, get_user_by_id, get_all_diets, get_all_goals, get_all_experience_levels, update_dob, update_height_weight, update_fitness_preferences, update_profile_picture, update_login_stats
from application.data_access.workouts_data_access import get_workout_video, get_exercises, get_sets, get_reps, \
    get_member_fitness_goal, get_member_experience, get_days_of_week, update_workout_progress, get_workout_progress
from application.data_access.dashboard_data_access import get_user_id, get_todays_meal_plan, get_todays_workout, get_latest_blogs, get_workout_progress_percent
from application.sample_data import quotes
import re
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from urllib.parse import unquote


@app.route('/')
@app.route('/home')
def home():
    """
    Renders the home page of the website. Checks if the user is logged in
    and adjusts the rendering based on their logged-in status.

    Returns:
        render_template: The home page with logged-in status information.
    """

    if not session.get('loggedIn'): # Check if user is logged in
        # If not logged in, render home page with loggedin=False
        return render_template('home.html', title='Home', loggedin=False)

    # If logged in, render home page with loggedin=True
    return render_template('home.html', title='Home', loggedin=True)


# <---- Sign up / membership ---->
@app.route('/membership', methods=['GET'])
def signup_form():
    """
    Renders the sign-up form for new users.

    Returns:
        render_template: The sign-up page for new users.
    """

    # Render the membership sign-up form
    return render_template('membership.html', title='Membership')


@app.route('/signup', methods=['GET', 'POST'])
def signup_submit():
    """
    Handles the submission of the sign-up form. Validates the user's input
    and adds a new member if the details are valid.

    Returns:
        render_template: A page confirming successful sign-up or showing an error message.
    """

    error = ""  # Variable to store general error messages
    error_email_exist = ""  # Variable to store email already existing error message

    if request.method == 'POST':
        # Get form data for user details
        userfirstname = request.form.get('userName')
        userlastname = request.form.get('userLastname')
        useremail = request.form.get('userEmail')
        userpassword = request.form.get('userPassword')
        hashed_password = generate_password_hash(userpassword) # Hash the password before storing

        # Validate form fields
        if len(useremail) == 0 or len(userpassword) == 0 or len(userfirstname) == 0 or len(userlastname) == 0:
            error = 'Please supply all fields'   # Error message if any field is missing
        elif add_member(userfirstname, userlastname, useremail, hashed_password):
            error_email_exist = 'Already part of the family! Log in instead 😊'   # Error if email already exists
        elif not re.match(r"^[A-Za-zÀ-ÿ\s'-]+$", userfirstname) or not re.match(r"^[A-Za-zÀ-ÿ\s'-]+$", userlastname):
            error = 'First name and last name can only contain letters, spaces, apostrophes (\'), and hyphens (-).'   # Name format validation
        else:
            add_member(userfirstname, userlastname, useremail, hashed_password)   # Add new member to the system
            return render_template('signedup.html')   # Show success page

    # Render the sign-up form with error messages if validation fails
    return render_template('membership.html', title='Sign Up', message = error, message_email_exist = error_email_exist)


# <---- Login.logout ---->
@app.route('/login', methods=['GET', 'POST'])
def signin_form():
    """
    Renders the login form for users to enter their credentials.

    Returns:
        render_template: The login page for users to input their credentials.
    """

    # Render the login form for the user
    return render_template('login.html', title='Login')


@app.route('/signin', methods=['GET', 'POST'])
def signin_submit():
    error = ""
    error_invalid_credentials = ""
    """
    Handles the login form submission. Validates user credentials and logs
    the user in if successful.

    Returns:
        render_template: The login page with error messages if invalid credentials
        or redirects to the profile if successful.
    """

    if request.method == 'POST':
        # Get form data for login
        useremail = request.form.get('userEmail')
        userpassword = request.form.get('userPassword')

        # Validate if fields are not empty
        if len(useremail) == 0 or len(userpassword) == 0:
            error = 'Please supply all fields'
        else:
            saved_details = get_details_by_email(useremail)   # Get user details by email

            if saved_details: # If email exists in the database
                stored_password = saved_details[0]   # Get the stored password
                session['email'] = saved_details[2]
                session['user'] = saved_details[1]
                session['user_id'] = saved_details[3]
                session['email_id'] = saved_details[4]
                session['loggedIn'] = True

                # Validate password against the stored hash
                if check_password_hash(stored_password, userpassword):
                    update_login_stats(session['user_id'])   # Update login stats if successful
                    return redirect(url_for('profile'))
                else:
                    error_invalid_credentials = 'Incorrect email or password. Please try again!'
            else:
                error_invalid_credentials = 'Incorrect email or password. Please try again!'
        # Render the login page with error messages
        return render_template('login.html', title='Sign In', message = error, message_invalid_credentials = error_invalid_credentials)
    # Render the login page when the method is GET
    return render_template('login.html', title='Sign In')


@app.route('/loggedout')
def logged_out():
    """
    Logs the user out by clearing session data and redirects to the home page.

    Returns:
        redirect: Redirects the user to the home page after logging out.
    """

    # Clear session data to log the user out
    session.pop('email', None)
    session.pop('user', None)
    session.pop('user_id', None)
    session['loggedIn'] = False
    return redirect(url_for('home'))


@app.route('/reset', methods=['GET', 'POST'])
def reset_form():
    """
    Renders the form for resetting the user's password. It ensures the user
    is logged in before proceeding and validates the reset request.

    Returns:
        render_template: The password reset page with any error messages.
    """

    if not session.get('loggedIn'):   # Ensure the user is logged in
        return redirect(url_for('signin_form'))

    # Initialize error variables for different types of errors
    error_missing = ""
    error_different_password = ""
    error_invalid_password = ""

    if request.method == 'POST':
        # Get the form data for the password reset
        current_password = request.form.get('currentPassword')
        new_password = request.form.get('newPassword')
        confirm_password = request.form.get('confirmPassword')
        member_id = session['user_id']

        if not member_id:
            return redirect(url_for('signin_form'))   # Ensure member ID is available
        else:
            password_details = get_password_details_by_id(member_id)   # Get the current password details from the database
            if password_details:                        # If not empty
                stored_password = password_details[0]   # Get the stored password hash
                if len(current_password) == 0 or len(new_password) == 0 or len(confirm_password) == 0:
                    error_missing = 'Please supply all fields'
                else:
                    if check_password_hash(stored_password, current_password):   # Check if current password match save password
                        if new_password == confirm_password:                      # Check if new password and confirm match
                            hashed_new_password = generate_password_hash(new_password)   # Hash the new password
                            change_password(hashed_new_password, member_id)              # Update the password
                            flash("Your password has been updated.")
                            return redirect(url_for('profile'))
                        else:
                            error_different_password = "Passwords do not match"
                    else:
                        error_invalid_password = "Incorrect Password, please try again"

    return render_template('reset.html', title='Reset', message_invalid_password=error_invalid_password, message_different_password=error_different_password, message_missing=error_missing)


@app.route('/delete', methods=['GET', 'POST'])
def delete_account_route():
    """
    Handles the deletion of the user's account. Requires the user to be logged in.
    Deletes user-related data and clears the session.

    Returns:
        render_template: The account deletion confirmation page.
    """

    if not session.get('loggedIn'):
        return redirect(url_for('signin_form'))

    if request.method == 'POST':
        # Get user details for deletion
       member_id = session.get('user_id')
       emailid = session.get('email_id')
       if not member_id:
           return redirect(url_for('signin_form'))
       else:
           # Delete the user's account and email from the system
           delete_account(member_id)
           delete_email(emailid)
           session.clear()   # Clear session data after deletion
           flash("Your account has been deleted.")
           return render_template('home.html', title='settings')

    return render_template('delete.html', title='Delete')


@app.route('/get_started', methods=['GET'])
def get_started():
    """
    Redirects the user based on their login status.

    If the user is logged in (i.e., session['loggedIn'] is True),
    they are redirected to their dashboard. Otherwise, they are
    redirected to the membership page to sign up or learn more.

    Returns:
        Response object: A redirect to the appropriate page based on login status.
    """

    if session.get('loggedIn'):
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('signup_form'))


# <--Newsletter subscription-->
@app.route('/subscribe', methods=['POST'])
def subscribe():
    """
    Handles the subscription process for the newsletter.
    - Checks if the provided email is valid.
    - Adds the email to the 'email' table if not already present.
    - Inserts the email into the 'newsletter' table if not already subscribed.
    - Provides feedback to the user via flash messages.

    Returns:
        redirect: Redirects the user back to the blog page after processing the subscription.
    """

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
            # If the email does not exist, insert it into the 'email' table
            cursor.execute("INSERT INTO email (email_address) VALUES (%s)", (email,))
            conn.commit()
            email_id = cursor.lastrowid   # Get the id of the newly inserted email

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
    """
    Renders the blog home page by retrieving blogs from the database.

    - If a category is provided as a query parameter, it filters blogs by that category.
    - If no category is provided, it retrieves all blogs.

    Returns:
        render_template: Renders the 'blog_home.html' template with the list of blogs.
    """

    # Retrieve the 'category' parameter
    category = request.args.get('category')

    # If no category is selected, it fetches all blogs
    blog_database = get_all_blogs(category)

    # Pass the list of blogs to the 'blog_home' template
    return render_template('blog/blog_home.html', blog_list=blog_database)


# <--individual blog based on the blog ID-->
@app.route('/blog/<int:blog_id>', methods=['GET'])
def view_blog(blog_id):
    """
    Renders the individual blog page by retrieving blog details from the database.

    - Takes the blog ID from the URL and fetches the corresponding blog from the database.
    - If no blog is found, redirects the user to the blog home page.

    Args:
        blog_id (int): The ID of the blog to be retrieved from the database.

    Returns:
        render_template: Renders the 'view_blog.html' template with the blog data, or
                         redirects to the blog home page if no blog is found.
    """

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
    """
    Route to show the meal planner form. Redirects to the dashboard if the user is logged in.
    If not logged in, redirects to the signin form.

    Returns:
    - Redirect to the meal plan dashboard if the user is logged in.
    - Redirect to the signin form if the user is not logged in.
    """

    if not get_user_id():
        return redirect(url_for('signin_form'))
    return redirect(url_for('meal_plan_dashboard'))


@app.route('/save_meal_plan', methods=['POST'])
def save_meal_plan():
    """
    Route to save the meal plan submitted from the meal planner form.
    Saves the user's meal plan data to the database and redirects to the dashboard.

    Returns:
    - Redirect to the meal plan dashboard with the newly saved meal plan's timestamp.
    - Redirect to the signin form if the user is not logged in.
    """

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
    """
    Route to display the user's meal plan dashboard.
    Displays a list of saved meal plans and allows users to select a specific plan to view.

    Returns:
    - Rendered HTML template 'meal_plan_dashboard.html' displaying the user's meal plans.
    - Redirect to the signin form if the user is not logged in.
    """

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
    """
    Route to view a specific meal plan by its timestamp.
    Displays the detailed view of the selected meal plan.

    Parameters:
    - timestamp (str): The timestamp of the meal plan to view.

    Returns:
    - Rendered HTML template 'view_meal_plan.html' displaying the selected meal plan.
    - Redirect to the meal plan dashboard if the meal plan is not found.
    """

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
    """
    Route to edit a specific meal plan. If the method is POST, updates the meal plan
    in the database with new details such as name, description, and meals for each day.

    Parameters:
    - timestamp (str): The timestamp of the meal plan to be edited.

    Returns:
    - Rendered HTML template: 'edit_meal_plan.html' with the selected meal plan and days.
    - Redirect to meal plan dashboard on successful update.
    """

    timestamp = unquote(timestamp)
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
        cursor.close()
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
    """
    Route to clone an existing meal plan. If the method is POST, inserts a new meal
    plan into the database based on the selected meal plan, including the name, description,
    and meals for each day.

    Parameters:
    - timestamp (str): The timestamp of the meal plan to be cloned.

    Returns:
    - Rendered HTML template: 'clone_meal_plan.html' with the selected meal plan and days.
    - Redirect to meal plan dashboard on successful cloning.
    """

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
        cursor.close()
        conn.close()

        flash("Meal Plan Cloned!", "success")
        return redirect(url_for('meal_plan_dashboard', timestamp=timestamp_new))

    return render_template('meal_plan/clone_meal_plan.html', selected_meal_plan=selected_meal_plan, days=DAYS)


# -------------------------------------------------------------------------------------------------------------- #

# <---- Profile and profile settings ---->

# Route to display the user profile
@app.route("/profile", methods=["GET"])
def profile():
    """
    Route to display the user's profile. If the user is logged in, retrieves the user's
    information from the database and updates the session with the latest profile picture.

    Returns:
    - Rendered HTML template: 'profile.html' displaying the user's profile information.
    - Redirect to the sign-in page if the user is not logged in.
    """

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
    """
    Route for displaying and handling the user's profile settings.

    - If the user is not logged in, redirects to the sign-in form.
    - Handles the form submissions to update the user's profile information:
        - Account Information: Updates the user's date of birth and validates the age (must be at least 18).
        - Body Metrics: Updates the user's height and weight.
        - Preferences: Updates the user's fitness goals, experience level, and diet preferences.

    After a successful update, the user is redirected to their settings page with a success message.
    """

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
        return redirect(url_for("profile_settings", updated=1))

    user = get_user_by_id(user_id)
    fitness_goals = get_all_goals()
    experiences = get_all_experience_levels()
    diets = get_all_diets()

    return render_template("profile_settings.html", user=user, fitness_goals=fitness_goals, experiences=experiences, diets=diets)


@app.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    """
    Route to handle uploading and updating the user's profile picture.

    - If the user is not logged in or the user_id is not in the session, redirects to the sign-in form.
    - Checks if a profile picture file is present in the request.
    - If no file is selected or uploaded, a warning message is shown.
    - If a valid file is uploaded:
        - The file is saved to the server in a specific directory.
        - The user's profile picture path in the database is updated.
        - The relative path to the saved file is stored in the session.
    - After successful upload, the user is redirected to their profile page with a success message.
    """

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

        # Absolute path for saving the image
        upload_folder = os.path.join(app.root_path, 'static', 'images', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        full_path = os.path.join(upload_folder, filename)

        # Relative path for use in <img src=""> (convert backslashes to slashes)
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
    """
    Route to view workout videos based on user-defined parameters.

    - Accepts three query parameters from the URL:
      - 'goal': Specifies the user's fitness goal (e.g., weight loss, strength training).
      - 'experience': Specifies the user's fitness experience level (e.g., beginner, intermediate).
      - 'time': Specifies the duration of the workout in minutes.

    - Retrieves the appropriate workout video based on the provided parameters using the get_workout_video function.
    - Renders the 'workout_videos.html' template, passing the video and title information to the template.

    Query parameters example:
    - /workouts?goal=weight_loss&experience=beginner&time=30

    Returns:
    - Renders the workout videos page with the appropriate workout video.
    """

    # request is a special object in flask that gives you access to data sent by the client (browser)
    # request.args is a dictionary-like object that holds all of the querey paramteres from the URL
    # example - .get('goal') retrieves the value of the goal parameter from the URL
    # goal is a parameter defined in user_data_access.py
    goal = request.args.get('goal')
    experience = request.args.get('experience')
    time = request.args.get('time')
    workout_video = get_workout_video(goal, experience, time)
    return render_template('workout_videos.html', video=workout_video, title='Workout Videos')


# Workout Plan
@app.route('/my_workouts', methods=['GET'])
def view_workout_plan():
    """
    Displays a personalized workout plan based on the user's fitness goal and experience level.

    - If the user is not logged in, redirects to the login page.
    - If the user has not selected a fitness goal or experience level, displays an error message.
    - Otherwise, retrieves and displays the user's workout plan, progress, and a workout video.

    Returns:
        Rendered 'member_workouts.html' template with workout plan, progress, and video or error messages.
    """

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
    """
    Marks the completion status of a user's workout for each day of the week (Monday to Saturday).

    This function processes a form submission where checkboxes correspond to the days of the week
    (Monday to Saturday). It checks if the user has completed the workout on a given day and updates
    the workout progress in the database accordingly. If a checkbox is checked, it marks the day as done,
    otherwise it marks it as not done.

    - Loops through days (Monday to Saturday) and updates the workout progress table in the database.
    - After updating the progress, redirects back to the 'my_workouts' page.

    Returns:
        Redirects to '/my_workouts' page after processing the form.
    """

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


# <---- Dashboard ---->
# FINAL ROUTE
@app.route("/dashboard")
def dashboard():
    """
    Route for the user dashboard.

    - Ensures the user is logged in by checking the session.
    - Retrieves and formats the current day and its number in the week.
    - Selects a random motivational quote.
    - Gathers data for the dashboard:
      - Today's meal plan
      - Today's workout
      - Workout progress percentage
      - Latest blog posts

    Returns:
    - Renders 'dashboard.html' with all the above data.
    """

    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")  # Redirect to login if user not logged in

    today_day = datetime.today().strftime('%A')  # For display in the dashboard
    day_number = datetime.today().isoweekday()

    motivational_quote = random.choice(quotes)

    # Pull today's data using your data_access functions
    todays_meals = get_todays_meal_plan(user_id)
    todays_workout = get_todays_workout(user_id)
    progress_percent = get_workout_progress_percent(user_id)
    latest_blogs = get_latest_blogs()

    return render_template(
        "dashboard.html", today=today_day, day_number=day_number, motivational_quote=motivational_quote, todays_meals=todays_meals, todays_workout=todays_workout, progress_percent=progress_percent, latest_blogs=latest_blogs)

# TEST ROUTE
# @app.route("/dashboard")
# def dashboard():
#     user_id = session.get("user_id")
#     if not user_id:
#         return redirect("/login")
#
#     # 🛠 TEMP: Set to Tuesday this week (change year/month/day accordingly)
#     test_date = datetime(2025, 4, 15)  # ← e.g., Tuesday, April 15, 2025
#
#     today_day = test_date.strftime('%A')
#     day_number = test_date.isoweekday()
#     motivational_quote = random.choice(quotes)
#
#     # ⬇️ Pass test_date into both functions
#     todays_meals = get_todays_meal_plan(user_id, date=test_date)
#     todays_workout = get_todays_workout(user_id, date=test_date)
#     progress_percent = get_workout_progress_percent(user_id)
#     latest_blogs = get_latest_blogs()
#
#     return render_template(
#         "dashboard.html",
#         today=today_day,
#         day_number=day_number,
#         motivational_quote=motivational_quote,
#         todays_meals=todays_meals,
#         todays_workout=todays_workout,
#         progress_percent=progress_percent,
#         latest_blogs=latest_blogs
#     )