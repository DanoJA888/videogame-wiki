#TODO(Project 1): Implement Backend according to the requirements.

from google.cloud import storage
import base64
import hashlib

class Backend:

    def __init__(self, storage_client = storage.Client()):
        self.storage_client = storage_client

      
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
        bucket = self.storage_client.get_bucket('wikicontent')
        if file_name:
            blob = bucket.blob(file_name)
            blob.name = file_name.split('/')[-1]
            blob.upload_from_filename(file_name)
            return 'File uploaded to blob'
        else:
            return 'Ineligible filename'

    def sign_up(self, user, pw):
        bucket = self.storage_client.get_bucket('userpasswordinfo')
        blobs = bucket.list_blobs()
        blob = None

        if user and pw:
            for item in blobs:
                if item.name == user + ".txt":
                    return None
            blob = bucket.blob(user + '.txt')
            with blob.open(mode='w') as file:
                file.write(str(hashlib.blake2b(pw.encode()).hexdigest()))
                return 'User data successfully created'
        else:
            return 'Enter missing user or password'
        
        

            
    def sign_in(self, user, pw):
        bucket = self.storage_client.get_bucket('userpasswordinfo')
        blobs = bucket.list_blobs()
        user_info = None
        user_and_password_match = [False, False]
        
        for blob in blobs:
            if user+'.txt' == blob.name:
                user_info = blob
                break
        
        if not user_info:
            return user_and_password_match
        
        user_and_password_match[0] = True
        check_password = None
       
        with user_info.open(mode = 'r') as file:
            check_password = file.read()
        hashed_pw = hashlib.blake2b(pw.encode()).hexdigest()
        if check_password == str(hashed_pw):
            user_and_password_match[-1] = True
        return user_and_password_match
        
    def get_image(self, name):
        bucket = self.storage_client.get_bucket('wikicontent')
        blobs = bucket.list_blobs()
        image = None
        for blob in blobs:
            if blob.name == name:
                with blob.open(mode = 'rb') as file:
                    image = base64.b64encode(file.read())
                break
        if not image:
            print('image not found')
        else:
            return image