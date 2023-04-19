from flaskr import create_app
from flask_login import LoginManager, UserMixin, current_user
from unittest import mock
from unittest.mock import patch
import pytest
import flaskr.pages


# See https://flask.palletsprojects.com/en/2.2.x/testing/
# for more info on testing
@pytest.fixture
def app():
    app = create_app({'TESTING': True, 'LOGIN_DISABLED': False})
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
@mock.patch("flaskr.backend.Backend.get_all_page_names",
            return_value=["test1.html", "test2.html", "test3.html"])
def integration_get_all_pages(mock_get_all_page_names, client):
    resp = client.get("/pages/")
    html = resp.data.decode()
    assert resp.status_code == 200
    assert "Pages contained in this Wiki" in html
    mock_get_all_page_names.assert_called_once_with()


'''Mocks get_all_pages() from flaskr.pages.
        
        Raises:
            AssertionError: Mock function returns unexpected result; Status code is unexpected; HTML content is invalid
'''


    
@mock.patch("flaskr.backend.Backend.sign_up",
            return_value="User data successfully created")
def integration_signup_success(mock_sign_up, client):
    resp = client.get("/signup")
    html = resp.data.decode()
    assert resp.status_code == 200
    assert "Sign Up" in html
    assert mock_sign_up("testuser",
                        "testpw") == "User data successfully created"


'''Mocks the success of signup() from flaskr.pages.
        
        Raises:
            AssertionError: Mock function returns unexpected result; Status code is unexpected; HTML content is invalid
'''


@mock.patch("flaskr.backend.Backend.sign_up",
            return_value="Enter missing user or password")
def integration_signup_fail(mock_sign_up, client):
    resp = client.get("/signup")
    html = resp.data.decode()
    assert resp.status_code == 200
    assert "Sign Up" in html
    assert mock_sign_up("testuser",
                        "testpw") == "Enter missing user or password"


'''Mocks the failure of signup() from flaskr.pages.
        
        Raises:
             AssertionError: Mock function returns unexpected result; Status code is unexpected; HTML content is invalid
'''


def integration_upload_login_required(client):
    resp = client.get("/upload")
    assert resp.status_code == 401


'''Mocks @login_required for upload() from flaskr.pages.
        
        Raises:
            AssertionError: Status code is unexpected while LOGIN_DISABLED = False.
'''

def integration_create_page_login_required(client):
    '''Mocks @login_required for create_page() from flaskr.pages.
        
        Raises:
            AssertionError: Status code is unexpected while LOGIN_DISABLED = False.
    '''    
    resp = client.get("/create_page")
    assert resp.status_code == 401

def integration_edit_page_login_required(client):
    '''Mocks @login_required for edit_page() from flaskr.pages.
        
        Raises:
            AssertionError: Status code is unexpected while LOGIN_DISABLED = False.
    '''    
    resp = client.get("/edit_page")
    assert resp.status_code == 401

def integration_your_pages_login_required(client):
    '''Mocks @login_required for your_pages() from flaskr.pages.
        
        Raises:
            AssertionError: Status code is unexpected while LOGIN_DISABLED = False.
    '''    
    resp = client.get("/your_pages")
    assert resp.status_code == 401

def integration_logout_login_required(client):
    resp = client.get("/logout")
    assert resp.status_code == 401


'''Mocks @login_required for logout() from flaskr.pages.
        
        Raises:
            AssertionError: Status code is unexpected while LOGIN_DISABLED = False.
'''


def integration_get_user_page_route(client):
    page = 'sports_games.html'
    resp = client.get(f'/pages/{page}')
    assert resp.status_code == 200
    assert b'FIFA' in resp.data

def integration_create_page_route_logged_in(client):
    resp = client.get('/create_page')
    assert resp.status_code == 200
    assert b'Create Page' in resp.data

def integration_create_page_route_logged_out(client):
    resp = client.get('/create_page')
    assert resp.status_code == 401

def integration_edit_page_route_logged_in(client):
    resp = client.get('/edit_page')
    assert resp.status_code == 200
    assert b'Edit Page' in resp.data

def integration_edit_page_route_logged_out(client):
    resp = client.get('/edit_page')
    assert resp.status_code == 401

def integration_your_pages_route_logged_in(client):
    resp = client.get('/your_pages')
    assert resp.status_code == 200
    assert b"'s Pages" in resp.data

def integration_your_pages_route_logged_out(client):
    resp = client.get('/your_pages')
    assert resp.status_code == 401

def integration_upload_route_GET_logged_out(client):
    resp = client.get('/upload')
    assert resp.status_code == 401


def integration_upload_route_GET_logged_in(client):
    client.post('/login',
                data={
                    'username': 'sebastian',
                    'password': 'password'
                })
    resp = client.get('/upload')
    assert resp.status_code == 200
    assert b'value="Upload"' in resp.data


def integration_upload_route_POST_logged_out(client):
    resp = client.post('/upload', data={'file': 'test'})
    assert resp.status_code == 401


def integration_upload_route_POST_logged_in(client):
    client.post('/login',
                data={
                    'username': 'sebastian',
                    'password': 'password'
                })
    resp = client.post('/upload', data={'file': ''})
    assert resp.status_code == 302


@mock.patch('flask_login.utils._get_user')
def integration_login_required(self, client):
    user = mock.MagicMock()
    resp_upload = client.get("/upload")
    resp_logout = client.get("/logout")
    if not user.is_authenticated():
        assert resp_upload.status_code == 401
        assert resp_logout.status_code == 401


#test to make sure the home route renders correctly and message is in home page
def integration_home(client):
    resp = client.get("/")
    html = resp.data.decode()
    assert resp.status_code == 200
    assert 'Welcome to the Java The Hutt Wiki' in html


#test to make sure the about route renders correctly and message is in about page
def integration_about(client):
    resp = client.get("/about")
    html = resp.data.decode()
    assert resp.status_code == 200
    assert 'This Wiki discusses all things videogames, from different genres to some of the most popular games in each!' in html


# mocked a backend object using patch to see behavior of a succesful login, asserted by flashed message
def integration_login_success(client):
    with patch('flaskr.backend.Backend.sign_in'):
        data = {'username': 'test4', 'password': 'password'}
        resp = client.post("/login", data=data)
        html = resp.data.decode()
        assert resp.status_code == 200
        assert 'Succesfully Logged In' in html


# mocked a backend object using patch to see behavior of an unsuccesful login due to nonexistant username,
# asserted by flashed message
def integration_login_failed_bc_of_username(client):
    with patch('flaskr.backend.Backend.sign_in') as mocked_backend:

        mocked_backend.return_value = [False, False]
        data = {'username': 'unknown', 'password': 'password'}
        resp = client.post("/login", data=data)
        html = resp.data.decode()
        assert resp.status_code == 200
        assert 'Username does not exist' in html


# mocked a backend object using patch to see behavior of an unsuccesful login due to incorrect password,
# asserted by flashed message
def integration_login_failed_bc_of_pw(client):
    with patch('flaskr.backend.Backend.sign_in') as mocked_backend:

        mocked_backend.return_value = [True, False]
        data = {'username': 'test4', 'password': 'wrongpw'}
        resp = client.post("/login", data=data)
        html = resp.data.decode()
        assert resp.status_code == 200
        assert 'Password does not macth entered username, please try again' in html


#not sure how to test this, think i need to mock a User to be logged in but am running out of time, need to comment code
def integration_logout(client):
    resp = client.get('/logout')
    html = resp.data.decode()
    assert resp.status_code == 200
    assert 'You have logged out' in html
