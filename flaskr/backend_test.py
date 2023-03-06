from flaskr.backend import Backend
from google.cloud import storage
from unittest import mock

# TODO(Project 1): Write tests for Backend methods.

'''
@mock.patch("google.cloud.storage.Client")
def test_upload(mock_client):
    test_filename = 'test.jpg'
    mock_client = mock.MagicMock()
    mock_bucket = mock_client.bucket.return_value
    mock_blobs = mock_bucket.list_blobs.return_value
    mock_blob = mock_bucket.blob(test_filename)
    
    if test_filename:
        assert mock_blob.upload_from_filename(test_filename)
'''
    

@mock.patch("google.cloud.storage.Client")
def test_sign_up_correct(mock_client):
    user = 'test_user'
    pw = 'test_pw'
    mock_client = mock.MagicMock()
    mock_bucket = mock_client.get_bucket.return_value
    mock_blobs = mock_bucket.list_blobs.return_value
    mock_blob = mock_bucket.blob("mock_blob")

    if mock_blob not in mock_blobs:
        if user and pw:
            mock_blob.name = user + '.txt'
        assert mock_blob.name == 'test_user.txt'

@mock.patch("google.cloud.storage.Client")
def test_sign_up_incorrect(mock_client):
    user = None
    pw = None
    mock_client = mock.MagicMock()
    mock_bucket = mock_client.get_bucket.return_value
    mock_blobs = mock_bucket.list_blobs.return_value
    mock_blob = mock_bucket.blob("mock_blob")

    if mock_blob not in mock_blobs:
        if user and pw:
            mock_blob.name = user + '.txt'
        assert mock_blob.name == 'test_user.txt'
        
