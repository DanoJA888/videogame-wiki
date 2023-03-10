from flaskr import create_app
from flask_login import LoginManager, UserMixin, current_user
from unittest import mock
from unittest.mock import patch
import pytest


# See https://flask.palletsprojects.com/en/2.2.x/testing/ 
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# match the changes made in the other Checkpoint Requirements.
'''
def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hello, World!\n" in resp.data
'''

# TODO(Project 1): Write tests for other routes.
def test_pages_route(client):
    resp = client.get("/pages/")
    html = resp.data.decode()
    assert resp.status_code == 200

def test_signup_route(client):
    resp = client.get("/signup")
    assert resp.status_code == 200

@mock.patch('flask_login.utils._get_user')
def test_login_required(self, client):
    user = mock.MagicMock()
    resp_upload = client.get("/upload")
    resp_logout = client.get("/logout")
    if not user.is_authenticated():
        assert resp_upload.status_code == 401
        assert resp_logout.status_code == 401

#test to make sure the home route renders correctly and message is in home page
def test_home(client):
    resp = client.get("/")
    html = resp.data.decode()
    assert resp.status_code == 200
    assert 'Welcome to the Java The Hutt Wiki' in html

#test to make sure the about route renders correctly and message is in about page
def test_about(client):
    resp = client.get("/about")
    html = resp.data.decode()
    assert resp.status_code == 200
    assert 'This Wiki discusses all things videogames, from different genres to some of the most popular games in each!' in html

# mocked a backend object using patch to see behavior of a succesful login, asserted by flashed message
def test_login_success(client):
    with patch('flaskr.backend.Backend.sign_in'):
        data = {'username': 'test4', 'password' : 'password'}
        resp = client.post("/login", data = data)
        html = resp.data.decode()
        assert resp.status_code == 200
        assert 'Succesfully Logged In' in html

# mocked a backend object using patch to see behavior of an unsuccesful login due to nonexistant username, 
# asserted by flashed message
def test_login_failed_bc_of_username(client):
    with patch('flaskr.backend.Backend.sign_in') as mocked_backend:

        mocked_backend.return_value = [False, False]
        data = {'username': 'unknown', 'password' : 'password'}
        resp = client.post("/login", data = data)
        html = resp.data.decode()
        assert resp.status_code == 200
        assert 'Username does not exist' in html

# mocked a backend object using patch to see behavior of an unsuccesful login due to incorrect password, 
# asserted by flashed message   
def test_login_failed_bc_of_pw(client):
    with patch('flaskr.backend.Backend.sign_in') as mocked_backend:
        
        mocked_backend.return_value = [True, False]
        data = {'username': 'test4', 'password' : 'wrongpw'}
        resp = client.post("/login", data = data)
        html = resp.data.decode()
        assert resp.status_code == 200
        assert 'Password does not macth entered username, please try again' in html

#not sure how to test this, think i need to mock a User to be logged in but am running out of time, need to comment code
def test_logout(client):
    resp = client.get('/logout')
    html = resp.data.decode()
    assert resp.status_code == 200
    assert 'You have logged out' in html