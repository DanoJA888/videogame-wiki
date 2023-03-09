from flaskr.backend import Backend
from google.cloud import storage
from unittest import mock
import pytest
import base64
import hashlib

@pytest.fixture
def mock_blob():
    def _foo(blob_name, blob_content):
        mock_blob = mock.MagicMock()
        mock_blob.name = blob_name
        mock_blob.open.return_value.__enter__.return_value.read.return_value = blob_content
        return mock_blob
    return _foo

def test_get_wiki_page_success(mock_blob):
    with mock.patch.object(Backend, '__init__', lambda x, y: None):
        backend = Backend(None)
        backend.storage_client = mock.MagicMock()
        backend.storage_client.bucket.return_value.get_blob.return_value = mock_blob('Blob', 'Blob content') # Blob/page exists
        page = backend.get_wiki_page('Test Page')
        assert page == ('Blob', 'Blob content')

def test_get_wiki_page_failure(mock_blob):
    with mock.patch.object(Backend, '__init__', lambda x, y: None):
        backend = Backend(None)
        backend.storage_client = mock.MagicMock()
        backend.storage_client.bucket.return_value.get_blob.return_value = None # Blob/page doesn't exist
        page = backend.get_wiki_page('Test Page')
        assert page == 'The page does not exist.'

def test_get_all_page_names_without_jpg(mock_blob):
    with mock.patch.object(Backend, '__init__', lambda x, y: None):
        backend = Backend(None)
        backend.storage_client = mock.MagicMock()
        backend.storage_client.bucket.return_value.list_blobs.return_value = [  mock_blob('p1.html', 'Blob content'),
                                                                                mock_blob('p2.html', 'Blob content'),
                                                                                mock_blob('p3.html', 'Blob content')
                                                                            ]
        page_names = backend.get_all_page_names()
        assert page_names == ['p1.html', 'p2.html', 'p3.html']

def test_get_all_page_names_with_jpg(mock_blob): #nit could be better named as test_get_all_page_names_ignores_jpg_files
    with mock.patch.object(Backend, '__init__', lambda x, y: None):
        backend = Backend(None)
        backend.storage_client = mock.MagicMock()
        backend.storage_client.bucket.return_value.list_blobs.return_value = [  mock_blob('p1.html', 'Blob content'),
                                                                                mock_blob('p2.html', 'Blob content'),
                                                                                mock_blob('i1.jpg', 'Blob content'),
                                                                                mock_blob('p3.html', 'Blob content')
                                                                            ]
        page_names = backend.get_all_page_names()
        assert page_names == ['p1.html', 'p2.html', 'p3.html']

@mock.patch("google.cloud.storage.Client")
def test_upload_success(mock_client):
    test_filename = 'uploads/test.jpg' #test data should have the closest thing being actually used. without this, the split logic will not be tested.
    mock_client = mock.MagicMock()
    mock_blob = mock.MagicMock()
    mock_bucket = mock.MagicMock()
    mock_client.get_bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    
    mock_backend = Backend(mock_client) # nit: you are passing a mock to the backend, the backend itself is not a mock. so naming it as mock_backend is misleading 
    assert mock_backend.upload(test_filename) == 'File uploaded to blob' #ok but if you have asserted if the blob is created with the filename at least, that would be a better test (I have updated this test roughly here for reference)
    mock_bucket.blob.assert_called_with("uploads/test.jpg")
    assert mock_blob.name == "test.jpg"
    mock_blob.upload_from_filename.assert_called_once_with("uploads/test.jpg")

# comment should be at the top of the method
'''Passes a mocked storage.Client to Backend to test the success of upload().
            Args:
                mock_client: the mocked storage.Client()
                
            Raises:
                AssertionError: Return value is unexpected.
'''

@mock.patch("google.cloud.storage.Client")
def test_upload_fail(mock_client):
    test_filename = ''
    mock_client = mock.MagicMock()
    mock_backend = Backend(mock_client) # Another case for file already exists would have forced to mock more objects.
    assert mock_backend.upload(test_filename) == 'Ineligible filename'

'''Passes a mocked storage.Client to Backend to test the failure of upload().
            Args:
                mock_client: the mocked storage.Client()

            Raises:
                AssertionError: Return value is unexpected.
'''
    
@mock.patch("google.cloud.storage.Client")
def test_sign_up_success(mock_client):
    user = 'test_user'
    pw = 'test_pw'
    mock_client = mock.MagicMock()
    mock_backend = Backend(mock_client)
    mock_bucket = mock.MagicMock()
    mock_blob = mock.MagicMock()
    mock_client.get_bucket.return_value = mock_bucket
    mock_bucket.list_blobs.return_value = [mock_blob]
    mock_bucket.blob.return_value = mock_blob
    mock_file = mock.MagicMock()
    mock_blob.open.return_value = mock_file
    # mock_bucket = mock_client.get_bucket # I guess you mean mock_client.get_bucket.return_value = mock_bucket?
    # mock_blob = mock_bucket.get_blob("test_user.txt").return_value
    # mock_blob = None
    assert mock_backend.sign_up(user, pw) == 'User data successfully created' # same comment as test_upload, there should be more mocks and assertions on the interactions to be able to call that this tests things properly.
    mock_bucket.blob.assert_called_with("test_user.txt")
    mock_blob.open.assert_called_with(mode="w") #if you can pass a mock for the hash function, you can even assert that the file is written with the hashed password!

'''Passes a mocked storage.Client to Backend to test the success of sign_up().
            Args:
                mock_client: the mocked storage.Client()

            Raises:
                AssertionError: Return value is unexpected.
'''

@mock.patch("google.cloud.storage.Client")
def test_sign_up_fail_user(mock_client):
    user = 'test_user'
    pw = ''
    mock_client = mock.MagicMock()
    mock_backend = Backend(mock_client) # same comment as above. 
    assert mock_backend.sign_up(user, pw) == 'Enter missing user or password'

'''Passes a mocked storage.Client to Backend to test the failure of sign_up() due to 'user' return value.
            Args:
                mock_client: the mocked storage.Client()

            Raises:
                AssertionError: Return value is unexpected.
'''

@mock.patch("google.cloud.storage.Client")
def test_sign_up_fail_pw(mock_client):
    user = ''
    pw = 'test_pw'
    mock_client = mock.MagicMock()
    mock_backend = Backend(mock_client) # same comment as the test_sign_up_success.
    assert mock_backend.sign_up(user, pw) == 'Enter missing user or password'

'''Passes a mocked storage.Client to Backend to test the failure of sign_up() due to 'pw' return value.
            Args:
                mock_client: the mocked storage.Client()

            Raises:
                AssertionError: Return value is unexpected.
'''
