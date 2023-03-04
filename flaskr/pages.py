from flask import render_template, redirect
from flaskr.backend import Backend

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

    @app.route("/pages/")
    def get_all_pages():
        
        '''Passes a list of all blobs from wikicontent into pages.html.
        
            Returns:
                A render of the pages.html file w/ the pages list passed in.
        '''

        b = Backend()
        pages = b.get_all_page_names()
        return render_template("pages.html", pages=pages)

    @app.route("/signup")
    def signup():
        pass