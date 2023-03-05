from flask import render_template, redirect, request, flash
from flaskr.backend import Backend
from werkzeug.utils import secure_filename
import os

def make_endpoints(app):

    username = ''

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        return render_template('main.html', username=username)

    @app.route("/pages/<page>")
    def get_user_page(page):
        '''Fetches page from backend.

        Args:
            page:
                The name of the page to be fetched.

        Returns:
            The page contents as a string.
        '''
        b = Backend()
        page = b.get_wiki_page(page)
        with page.open('r') as f:
            return f.read()

    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        '''Uploads user content to backend.

        Returns:
            Tha page contents as a string.
        '''
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
            elif file.filename.split('.')[-1] not in {'html', 'jpg'}:
                flash('File type not accepted')
                return redirect(request.url)
            b = Backend()
            filename = secure_filename(file.filename)
            if filename not in b.get_all_page_names() + b.get_all_image_names():
                filename = 'flaskr/uploads/' + filename
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

        b = Backend()
        pages = b.get_all_page_names()
        return render_template("pages.html", pages=pages)

    @app.route("/signup", methods =['GET', 'POST'])
    def signup():
        b = Backend()
        confirm = ""
        
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if not username or not password:
                confirm = "Please fill out all fields."
            if not b.sign_up(username, password):
                confirm = "Username already taken!"
            else:
                b.sign_up(username, password)
                confirm = "Successful sign-up!"
                
        
        return render_template("signup.html", confirm=confirm)
            
