from flask import render_template, redirect, request, flash, url_for, make_response
from flaskr.backend import Backend
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
from google.cloud import storage
import os


class User(UserMixin):

    def __init__(self, username, client, bucket):
        self.id = username
        self.username = username
        self.client = client
        self.bucket = bucket
        self.blob = self.bucket.get_blob(username + '.txt')

    def get(self, username):
        if self.blob:
            return User(self.id, self.client, self.bucket)
        return None


def make_endpoints(app, backend=Backend()):

    app.secret_key = "key"
    client = storage.Client()
    bucket = client.get_bucket('userpasswordinfo')

    login_manager = LoginManager()
    login_manager.init_app(app)
    b = backend

    @login_manager.user_loader
    def load_user(username):
        return User(username, client, bucket).get(username)

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        return render_template('main.html')

    @app.route("/pages/<page>")
    def get_user_page(page):
        '''Fetches page from backend.

        Args:
            page:
                The name of the page to be fetched.

        Returns:
            The specified page contents as a string.
        '''
        file_name, file_content = b.get_wiki_page(page)
        with open(file_path := f'flaskr/templates/{file_name}', 'w') as f:
            file_content = ''.join([
                '{% extends "main.html" %}', '{% block page_name %}',
                f'{file_name.split(".")[0]}', '{% endblock %}',
                '{% block content %}', file_content, '{% endblock %}'
            ])
            f.write(file_content)
        rendered_page = render_template(file_name)
        os.remove(file_path)
        return rendered_page

    '''
    route for the about page. I chose to have a list containing all our images as well as our names and zipping the values into one 
    list for templating ease using Jinja in the html, rendered the template with the list containing image/name
    **IMPORTANT** since i am returning an encoded string for the jpg, i decode it after reciving it from get_image in backend
    '''

    @app.route("/about", methods=['GET'])
    def about():
        images = [
            b.get_image("Daniel_Image.jpg").decode('utf-8'),
            b.get_image("Chris_Image.jpg").decode('utf-8'),
            b.get_image("Sebastian_Img.jpg").decode('utf-8')
        ]
        names = ["Daniel Aguilar", "Chris Cooper", "Sebastian Balderrama"]
        about_info = zip(names, images)
        return render_template("about.html", about_info=about_info)

    @app.route('/upload', methods=['GET', 'POST'])
    @login_required
    def upload():
        '''Uploads user content to backend.

        Returns:
            The upload page contents as a string.
        '''
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
            elif (file_extension :=
                  file.filename.split('.')[-1]) not in {'html', 'jpg'}:
                flash('File type not accepted')
                return redirect(request.url)
            filename = secure_filename(file.filename)
            if filename not in b.get_all_page_names() + b.get_all_image_names():
                filename = ''.join([
                    'flaskr/uploads/', request.form['wikiname'], '.',
                    file_extension
                ])
                if file_extension == 'html':
                    b.create_comment_section(filename)
                file.save(os.path.join(filename))
                b.upload(filename)
                os.remove(filename)
                flash('File uploaded')
            else:
                flash('This file already exists')
            return redirect(request.url)
        return render_template('upload.html')

    @app.route("/pages/")
    def get_all_pages():
        '''Passes a list of all blobs from wikicontent into pages.html.
        
            Returns:
                A render of the pages.html file w/ the pages list passed in.
        '''

        pages = b.get_all_page_names()
        return render_template("pages.html", pages=pages)

    @app.route("/signup", methods=['GET', 'POST'])
    def signup():

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if not username or not password:
                flash("Please fill out all fields.")
                return redirect(request.url)
            if not b.sign_up(username, password):
                flash("Username already taken!")
            else:
                b.sign_up(username, password)
                flash("Successful sign-up!")
            return redirect(request.url)
        return render_template("signup.html")

    '''Passes sign-up form information to backend to create user data.
        
        Returns:
            A render of the signup.html file w/ form content.
    '''
    '''
    Quite difficult for me tbh. pulled the entered info from the html form and called sign in to display different results and
    render the appropriate templates. What I had trouble with was the login manager, more so understanding it and applying it with User
    class
    '''

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            result_of_credential_input = b.sign_in(username, password)
            if result_of_credential_input[0] and result_of_credential_input[1]:
                u = User(username, client, bucket)
                login_user(u)
                flash('Succesfully Logged In')
                return render_template('main.html')
            elif not result_of_credential_input[0]:
                flash('Username does not exist')
                return render_template('login.html')
            else:
                flash(
                    'Password does not macth entered username, please try again'
                )
                return render_template('login.html')
        return render_template("login.html")

    '''logged out the user and flashed the message'''

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash('You have logged out')
        return render_template('logout.html')
