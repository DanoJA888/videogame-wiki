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
        return [blob.name for blob in blobs if blob.name.split('.')[-1] == 'html']

    # Returns a list of all the image names
    def get_all_image_names(self):
        storage_client = storage.Client()
        try:
            bucket = storage_client.bucket('wikicontent')
        except google.cloud.exceptions.NotFound:
            return 'bucket not found'
        blobs = bucket.list_blobs()
        return [blob.name for blob in blobs if blob.name.split('.')[-1] == 'jpg']

    def upload(self, file_name):
        client = storage.Client()
        bucket = client.get_bucket('wikicontent')
        blob = bucket.blob(file_name)
        blob.name = file_name.split('/')[-1]
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
            file.write(pw.hash())
            
    def sign_in(self, user, pw):
        client = storage.Client()
        bucket = client.get_bucket('userpasswordinfo')
        blobs = bucket.list_blobs()
        user_info = None
        for blob in blobs:
            if user == blob.name:
                user_info = blob
                break
        if not user_info:
            print('Username does not exist')
            return False
        username_and_password = None
        with user_info.open(mode = 'r') as file:
            for line in file:
                username_and_password = line.split(' ')
        if username_and_password[-1] == pw.hash():
            return True
        print('Password does not match')
        return False

        
    def get_image(self, name):
        client = storage.Client()
        bucket = client.get_bucket('wikicontent')
        blobs = bucket.list_blobs()
        for blob in blobs:
            if blob.name == name:
                return blob
        print('image not found')