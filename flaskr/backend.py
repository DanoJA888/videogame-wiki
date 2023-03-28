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
        blob = bucket.blob(file_name)
        blob.name = file_name.split('/')[-1]
        blob.upload_from_filename(file_name)

    def sign_up(self, user, pw):
        bucket = self.storage_client.get_bucket('userpasswordinfo')
        blobs = bucket.list_blobs()
        blob = None

        for item in blobs:
            if item.name == user + ".txt":
                return False
        
        blob = bucket.blob(user + '.txt')
        with blob.open(mode='w') as file:
            file.write(str(hashlib.blake2b(pw.encode()).hexdigest()))
            return True

    '''
    Got all the blobs from the bucket to find the user's info, in hindesight could have just checked if the blob existed,
    from there accounted for different things, return double false list if username wasnt found, 
    then if user existed I would read the file to get the password and hash it. 
    if hashed password didnt match the users pw, return true false meaning un was there but wrong pw
    anything else means the un and pw matched each other and we can return a double true list
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
        return user_and_password_match
    '''
    Similar to sign_in that instead of iterating through blobs could have just checked directly if it existed, oh well.
    if i found the image i would encode the bytes into a string so that i can return that and make it easier for myself later on
    after that, if i found no  image (if image is none) then I would return a none else i would return the encoded string
    '''    
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
            return None
        else:
            return image