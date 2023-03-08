from flaskr.backend import Backend
from unittest.mock import MagicMock
from unittest.mock import Mock
import hashlib

# TODO(Project 1): Write tests for Backend methods.

def test_sign_in_succeeds():
    user = 'test4'
    pw = 'password'
    
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob_list =[]
    mock_blob = MagicMock()
    mock_blob_list.append(mock_blob)
    mock_client.get_bucket.return_value = mock_bucket
    mock_bucket.list_blobs.return_value = mock_blob_list
    mock_blob.name = user+'.txt'
    mock_blob_open = MagicMock()
    mock_blob_open.__enter__.return_value.read.return_value = hashlib.blake2b(pw.encode()).hexdigest()
    mock_blob.open.return_value = mock_blob_open

    b  = Backend(mock_client)
    result = b.sign_in(user, pw)
    assert result == [True, True]

def test_sign_in_fails_bc_of_username():
    user = 'test4'
    pw = 'password'
    
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob_list =[]
    mock_blob = MagicMock()
    mock_blob_list.append(mock_blob)
    mock_client.get_bucket.return_value = mock_bucket
    mock_bucket.list_blobs.return_value = mock_blob_list
    mock_blob.name = 'test5'+'.txt'
    mock_blob_open = MagicMock()
    mock_blob_open.__enter__.return_value.read.return_value = hashlib.blake2b(pw.encode()).hexdigest()
    mock_blob.open.return_value = mock_blob_open

    b  = Backend(mock_client)
    result = b.sign_in(user, pw)
    assert result == [False, False]

def test_sign_in_fails_bc_of_password():
    user = 'test4'
    pw = 'password'
    
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob_list =[]
    mock_blob = MagicMock()
    mock_blob_list.append(mock_blob)
    mock_client.get_bucket.return_value = mock_bucket
    mock_bucket.list_blobs.return_value = mock_blob_list
    mock_blob.name = user +'.txt'
    mock_blob_open = MagicMock()
    mock_blob_open.__enter__.return_value.read.return_value = hashlib.blake2b('wrong_password'.encode()).hexdigest()
    mock_blob.open.return_value = mock_blob_open

    b  = Backend(mock_client)
    result = b.sign_in(user, pw)
    assert result == [True, False]