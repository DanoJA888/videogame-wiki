from flask import render_template, redirect, request
from flaskr.backend import Backend

def make_endpoints(app):

    username = None

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

    @app.route("/logout")
    def logout():
        if username:
            return render_template('main.html', username=None)
            
