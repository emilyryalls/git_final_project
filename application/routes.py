from application import app
from flask import render_template, request, redirect, url_for

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

# All blogs page including filter option
@app.route('/blog_home', methods=['GET', 'POST'])
def blogs():
    return render_template('blog_home.html')

@app.route('/create-blog', methods=['GET', 'POST'])
def create_blog():
    return render_template('create_blog.html')