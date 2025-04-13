from application import app
from flask import render_template, request, redirect, url_for
from application.data_access import get_all_blogs, add_member, get_password_by_email
from application.data_access import get_blog_by_id # keep only one line?
import os
import re
import json
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash



@app.route('/')
@app.route('/home')
def home():
    # session['SignIn'] = False
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
            error_email_exist = 'This email address is already part of the family! Please log in to continue.'
        elif not re.match("^[A-Za-zÀ-ÿ\s'-]+$", userfirstname) or not re.match("^[A-Za-zÀ-ÿ\s'-]+$", userlastname):
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


#              <---- Blogs ---->

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


#           <---- Meal planner ---->

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


# <-- We dont need this any more -->
# @app.route('/create-blog', methods=['GET', 'POST'])
# def create_blog():
#     return render_template('create_blog.html')