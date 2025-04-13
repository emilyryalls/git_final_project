from application import app
from flask import render_template, request, redirect, url_for, flash, session

from application.data_access import get_all_blogs
from application.data_access import get_blog_by_id
from application.user_data_access import get_user_by_id, update_profile_info

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


# Route to display all blogs and filter
@app.route('/blog_home', methods=['GET'])
def blogs():
    # Retrieve the 'category' parameter
    category = request.args.get('category')

    # If no category is selected, it fetches all blogs
    blog_database = get_all_blogs(category)

    # Pass the list of blogs to the 'blog_home' template
    return render_template('blog_home.html', blog_list=blog_database)


# Route to display an individual blog based on the blog ID
@app.route('/blog/<int:blog_id>', methods=['GET'])
def view_blog(blog_id):
    # Call the data access function to get the blog details
    blog = get_blog_by_id(blog_id)

    if blog is None:
        # If no blog is found, redirect to the blog home page or show a 404
        return redirect(url_for('blogs'))

    # Render the template for the individual blog, passing the blog data
    return render_template('view_blog.html', blog=blog)


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
    # TEMP: Assume user_id = 1 for development/testing
    user_id = 1
    user = get_user_by_id(user_id)
    return render_template("profile.html", user=user)


# Route to edit profile details on settings page
@app.route("/profile/settings", methods=["GET", "POST"])
def update_profile():
    # TEMP: Assume user_id = 1 for development/testing
    user_id = 1
    user = get_user_by_id(user_id)

    if request.method == "POST":
        dob = request.form.get("dob")
        height = request.form.get("height")
        weight = request.form.get("weight")
        goal = request.form.get("goal")

        update_profile_info(user_id, dob, height, weight, goal)
        flash("Profile updated successfully!")
        return redirect(url_for("profile"))

    return render_template("profile_settings.html", user=user, fitness_goals=fitness_goals)