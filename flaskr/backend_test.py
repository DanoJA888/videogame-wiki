from flaskr.backend import Backend
from google.cloud import storage
from unittest import mock

# TODO(Project 1): Write tests for Backend methods.

@mock.patch("google.cloud.storage.Client")
def test_upload_success(mock_client):
    test_filename = 'test.jpg'
    mock_client = mock.MagicMock()
    mock_backend = Backend(mock_client)
    assert mock_backend.upload(test_filename) == 'File uploaded to blob'

@mock.patch("google.cloud.storage.Client")
def test_upload_fail(mock_client):
    test_filename = ''
    mock_client = mock.MagicMock()
    mock_backend = Backend(mock_client)
    assert mock_backend.upload(test_filename) == 'Ineligible filename'
    
@mock.patch("google.cloud.storage.Client")
def test_sign_up_success(mock_client):
    user = 'test_user'
    pw = 'test_pw'
    mock_client = mock.MagicMock()
    mock_backend = Backend(mock_client)
    mock_bucket = mock_client.get_bucket
    mock_blob = mock_bucket.get_blob("test_user.txt").return_value
    mock_blob = None
    assert mock_backend.sign_up(user, pw) == 'User data successfully created'

@mock.patch("google.cloud.storage.Client")
def test_sign_up_fail_user(mock_client):
    user = 'test_user'
    pw = ''
    mock_client = mock.MagicMock()
    mock_backend = Backend(mock_client)
    assert mock_backend.sign_up(user, pw) == 'Enter missing user or password'

@mock.patch("google.cloud.storage.Client")
def test_sign_up_fail_pw(mock_client):
    user = ''
    pw = 'test_pw'
    mock_client = mock.MagicMock()
    mock_backend = Backend(mock_client)
    assert mock_backend.sign_up(user, pw) == 'Enter missing user or password'


        
