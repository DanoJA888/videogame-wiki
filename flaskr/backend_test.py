from flaskr.backend import Backend
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
