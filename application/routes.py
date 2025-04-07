from application import app
from flask import render_template, request, redirect, url_for

from application.data_access import get_all_blogs


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

# All blogs page including filter option
@app.route('/blog_home', methods=['GET'])
def blogs():
    blog_database = get_all_blogs()
    return render_template('blog_home.html', blog_home=blog_database)








@app.route('/create-blog', methods=['GET', 'POST'])
def create_blog():
    return render_template('create_blog.html')