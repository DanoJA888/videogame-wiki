from flaskr.backend import Backend
from unittest import mock
import pytest

@pytest.fixture
def mock_blob():
    mock_blob = mock.MagicMock()
    mock_blob.open.return_value.__enter__.return_value.read.return_value = 'Blob content'
    return mock_blob

def test_get_wiki_page_success(mock_blob):
    with mock.patch.object(Backend, '__init__', lambda x, y: None):
        backend = Backend(None)
        backend.storage_client = mock.MagicMock()
        backend.storage_client.bucket.return_value.get_blob.return_value = mock_blob # Blob/page exists
        page = backend.get_wiki_page('Test Page')
        assert page == 'Blob content'

def test_get_wiki_page_failure(mock_blob):
    with mock.patch.object(Backend, '__init__', lambda x, y: None):
        backend = Backend(None)
        backend.storage_client = mock.MagicMock()
        backend.storage_client.bucket.return_value.get_blob.return_value = None # Blob/page doesn't exist
        page = backend.get_wiki_page('Test Page')
        assert page == 'The page does not exist.'
