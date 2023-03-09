from flaskr import create_app
from unittest import mock
import pytest
import flaskr.pages


# See https://flask.palletsprojects.com/en/2.2.x/testing/ 
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'LOGIN_DISABLED': False
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# match the changes made in the other Checkpoint Requirements.

# TODO(Project 1): Write tests for other routes.
# why remove test_home_page?

@mock.patch("flaskr.backend.Backend.get_all_page_names", return_value=["test1.html", "test2.html", "test3.html"])
def test_get_all_pages(mock_get_all_page_names, client):
    resp = client.get("/pages/")
    html = resp.data.decode()
    assert resp.status_code == 200
    assert "Pages contained in this Wiki" in html 
    # nit: can add more assertions to verify if the pages list is displayed 
    assert "test1.html" in html
    assert "test2.html" in html
    assert "test3.html" in html
    mock_get_all_page_names.assert_called_once_with()

'''Mocks get_all_pages() from flaskr.pages.
        
        Raises:
            AssertionError: Mock function returns unexpected result; Status code is unexpected; HTML content is invalid
'''

# missing test for about/
# nit: missing test for navbar "Signup" should show when the user is not logged in & "upload" "logout" should show when the user is logged in
@mock.patch("flaskr.backend.Backend.sign_up", return_value="User data successfully created")    
def test_signup_success(mock_sign_up, client):
    resp = client.get("/signup")
    # you should be issuing a POST instead
    # resp = client.post(
      # "/signup", data={"username": "some_user", "password": "1234"})
    html = resp.data.decode()
    assert resp.status_code == 200
    assert "Sign Up" in html
    # no point asserting this when you are explicitly mocking the return value for this interaction
    # and this is actually calling the mock with testuser and testpw. Whereas if you have issued a POST like above,
    # you can checking if the backend method was called :
    # mock_sign_up.assert_called_with("some_user","1234")
    assert mock_sign_up("testuser", "testpw") == "User data successfully created"


'''Mocks the success of signup() from flaskr.pages.
        
        Raises:
            AssertionError: Mock function returns unexpected result; Status code is unexpected; HTML content is invalid
'''

@mock.patch("flaskr.backend.Backend.sign_up", return_value="Enter missing user or password")    
def test_signup_fail(mock_sign_up, client): # same comment as test_signup_success
    resp = client.get("/signup")
    html = resp.data.decode()
    assert resp.status_code == 200
    assert "Sign Up" in html
    assert mock_sign_up("testuser", "testpw") == "Enter missing user or password"

'''Mocks the failure of signup() from flaskr.pages.
        
        Raises:
             AssertionError: Mock function returns unexpected result; Status code is unexpected; HTML content is invalid
'''

def test_upload_login_required(client):
    resp = client.get("/upload")
    assert resp.status_code == 401

'''Mocks @login_required for upload() from flaskr.pages.
        
        Raises:
            AssertionError: Status code is unexpected while LOGIN_DISABLED = False.
'''
    
def test_logout_login_required(client):
    resp = client.get("/logout")
    assert resp.status_code == 401

'''Mocks @login_required for logout() from flaskr.pages.
        
        Raises:
            AssertionError: Status code is unexpected while LOGIN_DISABLED = False.
'''

def test_get_user_page_route(client): # this is actually an integration test. if you have mocked the backend's get_wiki_page to return some content and assert on that, it would have been a unit test
    page = 'sports_games.html'
    resp = client.get(f'/pages/{page}')
    assert resp.status_code == 200
    assert b'FIFA' in resp.data

def test_upload_route_GET_logged_out(client):
    resp = client.get('/upload')
    assert resp.status_code == 401

def test_upload_route_GET_logged_in(client):
    client.post('/login', data={ 'username' : 'sebastian', 'password' : 'password' })
    resp = client.get('/upload')
    assert resp.status_code == 200
    assert b'value="Upload"' in resp.data

def test_upload_route_POST_logged_out(client):
    resp = client.post('/upload', data={ 'file' : 'test'})
    assert resp.status_code == 401

def test_upload_route_POST_logged_in(client):
    client.post('/login', data={ 'username' : 'sebastian', 'password' : 'password' })
    resp = client.post('/upload', data={ 'file' : ''})
    assert resp.status_code == 302




    
