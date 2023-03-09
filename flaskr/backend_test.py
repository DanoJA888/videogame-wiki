from flaskr.backend import Backend
from google.cloud import storage
from unittest import mock
import pytest

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

def test_get_all_page_names_with_jpg(mock_blob):
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
    test_filename = 'test.jpg'
    mock_client = mock.MagicMock()
    mock_backend = Backend(mock_client)
    assert mock_backend.upload(test_filename) == 'File uploaded to blob'

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
    mock_backend = Backend(mock_client)
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
    mock_bucket = mock_client.get_bucket
    mock_blob = mock_bucket.get_blob("test_user.txt").return_value
    mock_blob = None
    assert mock_backend.sign_up(user, pw) == 'User data successfully created'

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
    mock_backend = Backend(mock_client)
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
    mock_backend = Backend(mock_client)
    assert mock_backend.sign_up(user, pw) == 'Enter missing user or password'

'''Passes a mocked storage.Client to Backend to test the failure of sign_up() due to 'pw' return value.
            Args:
                mock_client: the mocked storage.Client()

            Raises:
                AssertionError: Return value is unexpected.
'''
