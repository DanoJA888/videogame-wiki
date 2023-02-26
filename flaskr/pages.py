from flask import render_template, redirect
from flaskr.backend import Backend

def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template('main.html')

    # TODO(Project 1): Implement additional routes according to the project requirements.

    @app.route("/pages/<page>")
    def get_user_page(page):
        b = Backend()
        page = b.get_wiki_page(page)
        with page.open('r') as f:
            return f.read()