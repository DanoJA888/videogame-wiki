#TODO(Project 1): Implement Backend according to the requirements.

from google.cloud import storage
import base64
import hashlib

class Backend:

    def __init__(self, storage_client = storage.Client()):
        self.storage_client = storage_client

    # Returns the requested page
    def get_wiki_page(self, name):
        bucket = self.storage_client.bucket('wikicontent') # nit: the bucket names can be constant variables shared across all methods in backend.
        if not (blob := bucket.get_blob(name)):
            return 'The page does not exist.'
        with blob.open('r') as f:
            return blob.name, f.read()
        
    # Returns a list of all the page names
    def get_all_page_names(self):
        bucket = self.storage_client.bucket('wikicontent')
        blobs = bucket.list_blobs()
        return [blob.name for blob in blobs if blob.name.split('.')[-1] == 'html'] # nit: quite fragile. anybody can go to the bucket upload files with no extension directly. you can rather use `if blob.name.endswith(("html")):` Also, fun fact, you can use yield here. Search for "Python yield"

    # Returns a list of all the image names
    def get_all_image_names(self): #nit: this is technically not needed if you can move the is_exists logic into upload() - refer my comment at pages.py
        bucket = self.storage_client.bucket('wikicontent')
        blobs = bucket.list_blobs()
        return [blob.name for blob in blobs if blob.name.split('.')[-1] == 'jpg'] # nit: same comment in get_all_page_names

    def upload(self, file_name):
        bucket = self.storage_client.get_bucket('wikicontent')
        if file_name:
            blob = bucket.blob(file_name) 
            blob.name = file_name.split('/')[-1]
            blob.upload_from_filename(file_name) # ok but if you directly passed the blob_data here, 
            # you could just do this instead :
            # with blob.open('wb') as f: 
            #   f.write(blob_data)
            return 'File uploaded to blob'
        else:
            return 'Ineligible filename' # prefer raising ValueError
        # comment should be on the top of the method.
    '''Uploads file to bucket 'wikicontent' as a blob if file_name exists.
        
        Returns:
            Strings corresponding to expected results for unit testing.
    '''


    def sign_up(self, user, pw):
        bucket = self.storage_client.get_bucket('userpasswordinfo') #nit: bucket name can be a constant which is used across all places in this file.
        blobs = bucket.list_blobs()
        blob = None

        if user and pw:
            for item in blobs: # instead of iterating, you could just use get_blob(user + ".txt") and see if it not None
                if item.name == user + ".txt":
                    return None
            blob = bucket.blob(user + '.txt')
            with blob.open(mode='w') as file:
                file.write(str(hashlib.blake2b(pw.encode()).hexdigest()))
                return 'User data successfully created' 
        else:
            return 'Enter missing user or password' # prefer raising ValueError instead of returning error as strings. if the method doesn't throw any error, you can assume that signup succeeded in the tests (but with additional mock verifications)
    # nit comment should preceed the method
    '''Uploads file to bucket 'userpasswordinfo' as a blob containing userdata in the event of eligible user and password.
        
        Returns:
             Strings corresponding to expected results for unit testing.
    '''
        
        

            
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
        return user_and_password_match # prefer raising appropriate ValueErrors - for username not valid/password not matching cases
        
    def get_image(self, name):
        bucket = self.storage_client.get_bucket('wikicontent')
        blobs = bucket.list_blobs() # just use bucket.get_blob
        image = None
        for blob in blobs:
            if blob.name == name:
                with blob.open(mode = 'rb') as file:
                    image = base64.b64encode(file.read()) # nit: you can just use BytesIO from io package
                break
        if not image:
            print('image not found') # this code path should also have a return statement. Else it is different to add tests for this method.
        else:
            return image