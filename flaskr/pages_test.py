from flaskr import create_app
from flask_login import LoginManager, UserMixin, current_user
from unittest import mock
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
# '''
# def test_home_page(client):
#     resp = client.get("/")
#     assert resp.status_code == 200
#     assert b"Hello, World!\n" in resp.data
# '''

# # TODO(Project 1): Write tests for other routes.
# def test_pages_route(client):
#     resp = client.get("/pages/")
#     html = resp.data.decode()
#     assert resp.status_code == 200

# def test_signup_route(client):
#     resp = client.get("/signup")
#     assert resp.status_code == 200

# @mock.patch('flask_login.utils._get_user')
# def test_login_required(self, client):
#     user = mock.MagicMock()
#     resp_upload = client.get("/upload")
#     resp_logout = client.get("/logout")
#     if not user.is_authenticated():
#         assert resp_upload.status_code == 401
#         assert resp_logout.status_code == 401

def test_get_user_page_route(client):
    page = 'sports_games.html'
    resp = client.get(f'/pages/{page}')
    assert resp.status_code == 200
    assert b"FIFA" in resp.data

def test_upload_route_GET_logged_out(client):
    resp = client.get('/upload')
    assert resp.status_code == 401

def test_upload_route_GET_logged_in(client):
    client.post('/login', data={ 'username' : 'sebastian', 'password' : 'password' })
    resp = client.get('/upload')
    assert resp.status_code == 200
    assert b"value=Upload" in resp.data

def test_upload_route_POST_logged_out(client):
    resp = client.post('/upload', data={ 'file' : 'test'})
    assert resp.status_code == 401

def test_upload_route_POST_logged_in(client):
    client.post('/login', data={ 'username' : 'sebastian', 'password' : 'password' })
    resp = client.post('/upload', data={ 'file' : ''})
    assert resp.status_code == 302




    
