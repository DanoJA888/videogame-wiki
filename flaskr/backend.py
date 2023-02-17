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

    def upload(self, file_name):
        client = storage.Client()
        bucket = client.get_bucket('wikicontent')
        blob = bucket.blob(file_name)

        blob.upload_from_filename(file_name)


    def sign_up(self, user, pw):
        client = storage.Client()
        bucket = client.get_bucket('userpasswordinfo')
        blobs = bucket.list_blobs()
        blob = None

        for item in blobs:
            if item.name == user + ".txt":
                print('Username is already taken')
                return
        
        blob = bucket.blob(user + '.txt')
        with blob.open(mode='w') as file:
            file.write(user)
            file.write(" ")
            file.write(pw.hash())
        

    def sign_in(self):
        pass

    def get_image(self):
        pass