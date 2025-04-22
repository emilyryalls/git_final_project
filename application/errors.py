from flask import render_template
from application import app
from application.exceptions.experience_exception import ExperienceException
from application.exceptions.goal_and_experience_exception import GoalAndExperienceException
from application.exceptions.goal_exception import GoalException


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(GoalAndExperienceException)
def handle_goal_and_experience_exception(error):
    return render_template("member_workouts.html", error_message=error), 400

@app.errorhandler(GoalException)
def handle_goal_exception(error):
    return render_template("member_workouts.html", error_message=error), 400

@app.errorhandler(ExperienceException)
def handle_experience_exception(error):
    return render_template("member_workouts.html", error_message=error), 400
