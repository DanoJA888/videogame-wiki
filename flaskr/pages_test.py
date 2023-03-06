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



    
