# TODO(Project 1): Implement Backend according to the requirements.

from google.cloud import storage

class Backend:

    def __init__(self):
        pass
        
    # Returns the requested page
    def get_wiki_page(self, name):
        storage_client = storage.Client()
        try:
            bucket = storage_client.bucket('wikicontent')
        except google.cloud.exceptions.NotFound:
            return 'bucket not found'
        blob = bucket.blob(name)
        return blob if blob else 'page not found'

    # Returns a list of all the page names
    def get_all_page_names(self):
        storage_client = storage.Client()
        try:
            bucket = storage_client.bucket('wikicontent')
        except google.cloud.exceptions.NotFound:
            return 'bucket not found'
        blobs = bucket.list_blobs()
        return [blob.name for blob in blobs]

    def upload(self):
        pass

    def sign_up(self):
        pass

    def sign_in(self):
        pass

    def get_image(self):
        pass