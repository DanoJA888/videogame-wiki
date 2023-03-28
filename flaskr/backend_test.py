from flaskr.backend import Backend
from unittest.mock import MagicMock
from unittest.mock import Mock
import hashlib
import base64

# TODO(Project 1): Write tests for Backend methods.

# extremely complicated mock, helped by Russ (SDS Section LA) to mock the client, bucket, blob list, and open, was told by Russ
# that I didnt have to mock the hashing function or the base 64 encoding
# testing output of sign_in method returns a succesful log in based on mocked blob(usern/pw) and expected result([true,true]), 
# very hard to do :(
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

# testing output of sign_in method returns a failed log in based on mocked blob(usern/pw)(non-existant un) and 
# expected result[false,false], very hard to do :(
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

# testing output of sign_in method returns a failed log in based on mocked blob(usern/pw)(wrong pw) and expected result[true,false], 
# very hard to do :(
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
    mock_blob_open.__enter__.return_value.read.return_value = hashlib.blake2b(pw.encode()).hexdigest()
    mock_blob.open.return_value = mock_blob_open

    b  = Backend(mock_client)
    result = b.sign_in(user, 'wrongpassword')
    assert result == [True, False]
# tried mocking in smiliar fashion, could not figure out how to pass a jpg!, sadly i think if i had the approriate file passed,
# the test would have worked, but couldnt get it and focused on other tests
'''
def test_get_image_success():
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob_list =[]
    mock_blob = MagicMock()
    mock_blob_list.append(mock_blob)
    mock_client.get_bucket.return_value = mock_bucket
    mock_bucket.list_blobs.return_value = mock_blob_list
    mock_blob.name = 'imageworks.jpg'.encode('utf-8')
    mock_blob_open = MagicMock()
    mock_blob_open.__enter__.return_value.read.return_value = base64.b64encode('imageworks.jpg'.encode('utf-8'))
    mock_blob.open.return_value = mock_blob_open
    b = Backend(mock_client)
    result = b.get_image('imageworks.jpg'.encode('utf-8'))
    assert result == base64.b64encode('imageworks.jpg'.encode('utf-8'))
'''