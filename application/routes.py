from application import app
from flask import render_template, request, redirect, url_for

from application.data_access import get_all_blogs
from application.data_access import get_blog_by_id

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/membership')
def membership():
    return render_template('membership.html', title='Membership')

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





# <-- We dont need this any more -->
# @app.route('/create-blog', methods=['GET', 'POST'])
# def create_blog():
#     return render_template('create_blog.html')