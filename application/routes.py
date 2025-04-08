from application import app
from flask import render_template, request, redirect, url_for

from application.data_access import get_all_blogs


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

# # All blogs page
# @app.route('/blog_home', methods=['GET'])
# def blogs():
#     blog_database = get_all_blogs()
#     return render_template('blog_home.html', blog_list=blog_database)


@app.route('/blog_home', methods=['GET'])
def blogs():
    # Retrieve the 'category' parameter
    category = request.args.get('category')

    # If no category is selected, it fetches all blogs
    blog_database = get_all_blogs(category)

    # Pass the list of blogs to the 'blog_home' template
    return render_template('blog_home.html', blog_list=blog_database)


# @app.route('/create-blog', methods=['GET', 'POST'])
# def create_blog():
#     return render_template('create_blog.html')