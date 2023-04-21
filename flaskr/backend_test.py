from flaskr.backend import Backend
from google.cloud import storage
from unittest import mock
import pytest
from unittest.mock import MagicMock
from unittest.mock import Mock
import hashlib
import base64
import json


@pytest.fixture
def mock_blob():

    def _foo(blob_name, blob_content):
        mock_blob = mock.MagicMock()
        mock_blob.name = blob_name
        mock_blob.open.return_value.__enter__.return_value.read.return_value = blob_content
        return mock_blob

    return _foo


# def test_get_wiki_page_success(mock_blob):
#     with mock.patch.object(Backend, '__init__', lambda x, y: None):
#         backend = Backend(None)
#         backend.storage_client = mock.MagicMock()
#         backend.storage_client.bucket.return_value.get_blob.return_value = mock_blob(
#             'Blob', 'Blob content')  # Blob/page exists
#         page = backend.get_wiki_page('Test Page')
#         assert page == ('Blob', 'Blob content')

# def test_get_wiki_page_failure(mock_blob):
#     with mock.patch.object(Backend, '__init__', lambda x, y: None):
#         backend = Backend(None)
#         backend.storage_client = mock.MagicMock()
#         backend.storage_client.bucket.return_value.get_blob.return_value = None  # Blob/page doesn't exist
#         page = backend.get_wiki_page('Test Page')
#         assert page == 'The page does not exist.'


@mock.patch("google.cloud.storage.Client")
def test_get_wiki_page_valid_page(client):
    # pagevoters
    pagevoters_blob = MagicMock()
    pagevoters_bucket = MagicMock()
    pagevoters_blob.open.return_value.__enter__.return_value.read.return_value = json.dumps(
        {'user': 1})
    pagevoters_bucket.get_blob.return_value = pagevoters_blob
    # pagerankings
    pagerankings_blob = MagicMock()
    pagerankings_bucket = MagicMock()
    pagerankings_blob.open.return_value.__enter__.return_value.read.return_value = '5'
    pagerankings_bucket.get_blob.return_value = pagerankings_blob
    # wikicontent
    wikicontent_blob = MagicMock()
    wikicontent_bucket = MagicMock()
    wikicontent_blob.open.return_value.__enter__.return_value.read.return_value = 'page content'
    wikicontent_blob.name = 'page'
    wikicontent_bucket.get_blob.return_value = wikicontent_blob

    # allows get_bucket to return a certain bucket depending on the input
    def get_bucket_side_effect(bucket_name):
        return {
            'wikicontent': wikicontent_bucket,
            'pagerankings': pagerankings_bucket,
            'pagevoters': pagevoters_bucket
        }[bucket_name]

    client.get_bucket.side_effect = get_bucket_side_effect
    backend = Backend(client)

    get_wiki_page_return = backend.get_wiki_page('page', 'user')

    wikicontent_bucket.get_blob.assert_called_once_with('page')
    pagerankings_bucket.get_blob.assert_called_once_with('page')
    pagevoters_bucket.get_blob.assert_called_once_with('page')
    assert get_wiki_page_return == ('page', 'page content', 5, 1)


@mock.patch("google.cloud.storage.Client")
def test_get_wiki_page_invalid_page(client):
    # pagevoters
    pagevoters_blob = MagicMock()
    pagevoters_bucket = MagicMock()
    pagevoters_blob.open.return_value.__enter__.return_value.read.return_value = json.dumps(
        {'user': 1})
    pagevoters_bucket.get_blob.return_value = pagevoters_blob
    # pagerankings
    pagerankings_blob = MagicMock()
    pagerankings_bucket = MagicMock()
    pagerankings_blob.open.return_value.__enter__.return_value.read.return_value = '5'
    pagerankings_bucket.get_blob.return_value = pagerankings_blob
    # wikicontent
    wikicontent_blob = MagicMock()
    wikicontent_bucket = MagicMock()
    wikicontent_blob.open.return_value.__enter__.return_value.read.return_value = None
    wikicontent_blob.name = None
    wikicontent_bucket.get_blob.return_value = None

    # allows get_bucket to return a certain bucket depending on the input
    def get_bucket_side_effect(bucket_name):
        return {
            'wikicontent': wikicontent_bucket,
            'pagerankings': pagerankings_bucket,
            'pagevoters': pagevoters_bucket
        }[bucket_name]

    client.get_bucket.side_effect = get_bucket_side_effect
    backend = Backend(client)

    get_wiki_page_return = backend.get_wiki_page('page', 'user')

    wikicontent_bucket.get_blob.assert_called_once_with('page')
    pagerankings_bucket.get_blob.assert_not_called()
    pagevoters_bucket.get_blob.assert_not_called()
    assert get_wiki_page_return == 'The page does not exist.'


@mock.patch("google.cloud.storage.Client")
def test_get_wiki_page_user_not_logged_in(client):
    # pagevoters
    pagevoters_blob = MagicMock()
    pagevoters_bucket = MagicMock()
    pagevoters_blob.open.return_value.__enter__.return_value.read.return_value = json.dumps(
        {'user': 1})
    pagevoters_bucket.get_blob.return_value = pagevoters_blob
    # pagerankings
    pagerankings_blob = MagicMock()
    pagerankings_bucket = MagicMock()
    pagerankings_blob.open.return_value.__enter__.return_value.read.return_value = '5'
    pagerankings_bucket.get_blob.return_value = pagerankings_blob
    # wikicontent
    wikicontent_blob = MagicMock()
    wikicontent_bucket = MagicMock()
    wikicontent_blob.open.return_value.__enter__.return_value.read.return_value = 'page content'
    wikicontent_blob.name = 'page'
    wikicontent_bucket.get_blob.return_value = wikicontent_blob

    # allows get_bucket to return a certain bucket depending on the input
    def get_bucket_side_effect(bucket_name):
        return {
            'wikicontent': wikicontent_bucket,
            'pagerankings': pagerankings_bucket,
            'pagevoters': pagevoters_bucket
        }[bucket_name]

    client.get_bucket.side_effect = get_bucket_side_effect
    backend = Backend(client)

    get_wiki_page_return = backend.get_wiki_page('page', None)

    wikicontent_bucket.get_blob.assert_called_once_with('page')
    pagerankings_bucket.get_blob.assert_called_once_with('page')
    pagevoters_bucket.get_blob.assert_called_once_with('page')
    assert get_wiki_page_return == ('page', 'page content', 5, 0)


def test_get_all_page_names_without_jpg(mock_blob):
    with mock.patch.object(Backend, '__init__', lambda x, y: None):
        backend = Backend(None)
        backend.storage_client = mock.MagicMock()
        backend.storage_client.bucket.return_value.list_blobs.return_value = [
            mock_blob('p1.html', 'Blob content'),
            mock_blob('p2.html', 'Blob content'),
            mock_blob('p3.html', 'Blob content')
        ]
        page_names = backend.get_all_page_names()
        assert page_names == ['p1.html', 'p2.html', 'p3.html']


def test_get_all_page_names_with_jpg(mock_blob):
    with mock.patch.object(Backend, '__init__', lambda x, y: None):
        backend = Backend(None)
        backend.storage_client = mock.MagicMock()
        backend.storage_client.bucket.return_value.list_blobs.return_value = [
            mock_blob('p1.html', 'Blob content'),
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
    mock_blob_list = []
    mock_blob = MagicMock()
    mock_blob_list.append(mock_blob)
    mock_client.get_bucket.return_value = mock_bucket
    mock_bucket.list_blobs.return_value = mock_blob_list
    mock_blob.name = user + '.txt'
    mock_blob_open = MagicMock()
    mock_blob_open.__enter__.return_value.read.return_value = hashlib.blake2b(
        pw.encode()).hexdigest()
    mock_blob.open.return_value = mock_blob_open

    b = Backend(mock_client)
    result = b.sign_in(user, pw)
    assert result == [True, True]


# testing output of sign_in method returns a failed log in based on mocked blob(usern/pw)(non-existant un) and
# expected result[false,false], very hard to do :(
def test_sign_in_fails_bc_of_username():
    user = 'test4'
    pw = 'password'

    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob_list = []
    mock_blob = MagicMock()
    mock_blob_list.append(mock_blob)
    mock_client.get_bucket.return_value = mock_bucket
    mock_bucket.list_blobs.return_value = mock_blob_list
    mock_blob.name = 'test5' + '.txt'
    mock_blob_open = MagicMock()
    mock_blob_open.__enter__.return_value.read.return_value = hashlib.blake2b(
        pw.encode()).hexdigest()
    mock_blob.open.return_value = mock_blob_open

    b = Backend(mock_client)
    result = b.sign_in(user, pw)
    assert result == [False, False]


# testing output of sign_in method returns a failed log in based on mocked blob(usern/pw)(wrong pw) and expected result[true,false],
# very hard to do :(
def test_sign_in_fails_bc_of_password():
    user = 'test4'
    pw = 'password'

    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob_list = []
    mock_blob = MagicMock()
    mock_blob_list.append(mock_blob)
    mock_client.get_bucket.return_value = mock_bucket
    mock_bucket.list_blobs.return_value = mock_blob_list
    mock_blob.name = user + '.txt'
    mock_blob_open = MagicMock()
    mock_blob_open.__enter__.return_value.read.return_value = hashlib.blake2b(
        pw.encode()).hexdigest()
    mock_blob.open.return_value = mock_blob_open

    b = Backend(mock_client)
    result = b.sign_in(user, 'wrongpassword')
    assert result == [True, False]


# unit test that checks the success of a valid comment
def test_make_comment_success():
    username = 'daniel'
    page_name = 'whatever.json'
    comment = 'this is a test'
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_client.get_bucket.return_value = mock_bucket
    mock_bucket.get_blob.return_value = mock_blob
    mock_blob.download_as_text.return_value = '[]'

    b = Backend(mock_client)
    result = b.make_comment(page_name, username, comment)
    assert result == [('daniel', 'this is a test')]


# unit test that checks the failure of an invalid comment
def test_make_comment_fails():
    username = 'this should pass and print empty list'
    page_name = 'whatever.json'
    comment = ''
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_client.get_bucket.return_value = mock_bucket
    mock_bucket.get_blob.return_value = mock_blob
    mock_blob.download_as_text.return_value = '[]'

    b = Backend(mock_client)
    result = b.make_comment(page_name, username, comment)
    assert result == []


#unit tests that checks the success of an existing comment section being returned
def test_get_comments_success():
    name = 'whatever.json'
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_client.get_bucket.return_value = mock_bucket
    mock_bucket.get_blob.return_value = mock_blob
    mock_blob.download_as_text.return_value = '[]'

    b = Backend(mock_client)
    result = b.get_section(name)
    assert result == []


#unit test that checks the correct message is sent if a comment doesnt exist
def test_get_comments_fail():
    name = 'unvalid'
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_client.get_bucket.return_value = mock_bucket
    mock_bucket.get_blob.return_value = None
    mock_blob.download_as_text.return_value = '[]'

    b = Backend(mock_client)
    result = b.get_section(name)
    assert result == 'Comment Section Not Found'


# unit test that checks for correct message if the comment section is correctly created with a valid name
def test_create_comment_section_success():
    name = 'flaskr/uploads/whatever.html'
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_client.get_bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob

    b = Backend(mock_client)
    result = b.create_comment_section(name)
    assert result == 'Comment Section Created'


# unit test that checks for correct message if the comment section is incorrectly created without a valid name
def test_create_comment_section_fail():
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_client.get_bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob

    b = Backend(mock_client)
    result = b.create_comment_section()
    assert result == 'Could Not Create Comment Section'


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


@mock.patch("google.cloud.storage.Client")
def test_update_vote_duplicate_vote(client):
    # pagevoters
    pagevoters_blob = MagicMock()
    pagevoters_bucket = MagicMock()
    pagevoters_blob.open.return_value.__enter__.return_value.read.return_value = json.dumps(
        {'user': 1})
    pagevoters_bucket.get_blob.return_value = pagevoters_blob
    # pagerankings
    pagerankings_blob = MagicMock()
    pagerankings_bucket = MagicMock()
    pagerankings_blob.open.return_value.__enter__.return_value.read.return_value = '5'
    pagerankings_bucket.get_blob.return_value = pagerankings_blob

    def get_bucket_side_effect(bucket_name):
        return pagevoters_bucket if bucket_name == 'pagevoters' else pagerankings_bucket

    client.get_bucket.side_effect = get_bucket_side_effect
    backend = Backend(client)
    #
    backend.update_vote('page', 'user', 1)
    pagevoters_blob.upload_from_string.assert_called_once_with(
        json.dumps({'user': 0}))
    pagerankings_blob.upload_from_string.assert_called_once_with('4')


@mock.patch("google.cloud.storage.Client")
def test_update_vote_change_vote(client):
    # pagevoters
    pagevoters_blob = MagicMock()
    pagevoters_bucket = MagicMock()
    pagevoters_blob.open.return_value.__enter__.return_value.read.return_value = json.dumps(
        {'user': 1})
    pagevoters_bucket.get_blob.return_value = pagevoters_blob
    # pagerankings
    pagerankings_blob = MagicMock()
    pagerankings_bucket = MagicMock()
    pagerankings_blob.open.return_value.__enter__.return_value.read.return_value = '5'
    pagerankings_bucket.get_blob.return_value = pagerankings_blob

    def get_bucket_side_effect(bucket_name):
        return pagevoters_bucket if bucket_name == 'pagevoters' else pagerankings_bucket

    client.get_bucket.side_effect = get_bucket_side_effect
    backend = Backend(client)
    #
    backend.update_vote('page', 'user', -1)
    pagevoters_blob.upload_from_string.assert_called_once_with(
        json.dumps({'user': -1}))
    pagerankings_blob.upload_from_string.assert_called_once_with('3')


@mock.patch("google.cloud.storage.Client")
def test_update_vote_new_user(client):
    # pagevoters
    pagevoters_blob = MagicMock()
    pagevoters_bucket = MagicMock()
    pagevoters_blob.open.return_value.__enter__.return_value.read.return_value = json.dumps(
        {'user1': 1})
    pagevoters_bucket.get_blob.return_value = pagevoters_blob
    # pagerankings
    pagerankings_blob = MagicMock()
    pagerankings_bucket = MagicMock()
    pagerankings_blob.open.return_value.__enter__.return_value.read.return_value = '5'
    pagerankings_bucket.get_blob.return_value = pagerankings_blob

    # allows get_bucket to return a certain bucket depending on the input
    def get_bucket_side_effect(bucket_name):
        return pagevoters_bucket if bucket_name == 'pagevoters' else pagerankings_bucket

    client.get_bucket.side_effect = get_bucket_side_effect
    backend = Backend(client)
    #
    backend.update_vote('page', 'user2', 1)
    pagevoters_blob.upload_from_string.assert_called_once_with(
        json.dumps({
            'user1': 1,
            'user2': 1
        }))
    pagerankings_blob.upload_from_string.assert_called_once_with('6')


@mock.patch("google.cloud.storage.Client")
def test_get_page_rankings(client):
    blob1 = MagicMock()
    blob1.name = 'page1'
    blob1.open.return_value.__enter__.return_value.read.return_value = '5'
    blob2 = MagicMock()
    blob2.name = 'page2'
    blob2.open.return_value.__enter__.return_value.read.return_value = '10'
    bucket = MagicMock()
    bucket.list_blobs.return_value = [blob1, blob2]
    client = MagicMock()
    client.get_bucket.return_value = bucket
    backend = Backend(client)
    backend.num_pages_to_show = 1
    page_rankings = backend.get_page_rankings()
    assert backend.page_rankings == [('page2', 10), ('page1', 5)]
    assert page_rankings == ['page2']
