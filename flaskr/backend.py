#TODO(Project 1): Implement Backend according to the requirements.

from google.cloud import storage
import base64
import hashlib
import json


class Backend:

    def __init__(self, storage_client=storage.Client()):
        self.storage_client = storage_client
        self.page_rankings = []
        self.num_pages_to_show = 0

    # Returns the requested page
    def get_wiki_page(self, name):
        '''Fetches blob from wikicontent bucket in google clous storage

        Args:
            name:
                The name of the blob to be fetched.

        Returns:
            The name of the blob and its contents as a string.
        '''
        bucket = self.storage_client.bucket('wikicontent')
        if not (blob := bucket.get_blob(name)):
            return 'The page does not exist.'
        with blob.open('r') as f:
            return blob.name, f.read()

    # Returns a list of all the page names
    def get_all_page_names(self):
        '''Fetches all blobs from wikicontent bucket in google cloud storage
        that contain an html page.

        Returns:
            A list of the page names as strings.
        '''

        bucket = self.storage_client.bucket('wikicontent')
        blobs = bucket.list_blobs()
        return [
            blob.name for blob in blobs if blob.name.split('.')[-1] == 'html'
        ]

    # Returns a list of all the image names
    def get_all_image_names(self):
        '''Fetches all blobs from wikicontent bucket in google cloud storage
        that contain an jpg image.

        Returns:
            A list of the image names as strings.
        '''
        bucket = self.storage_client.bucket('wikicontent')
        blobs = bucket.list_blobs()
        return [
            blob.name for blob in blobs if blob.name.split('.')[-1] == 'jpg'
        ]

    def upload(self, file_name):
        wiki_content_bucket = self.storage_client.get_bucket('wikicontent')
        page_voters_bucket = self.storage_client.get_bucket('pagevoters')
        page_rankings_bucket = self.storage_client.get_bucket('pagerankings')
        if file_name:
            # uploads page
            blob = wiki_content_bucket.blob(file_name)
            blob.name = file_name.split('/')[-1]
            blob.upload_from_filename(file_name)
            # allows page voting records to be stored for this page
            blob = page_voters_bucket.blob(file_name.split('/')[-1])
            blob.name = file_name.split('/')[-1]
            blob.upload_from_string(json.dumps({}))
            # allows page rank to be tracked fpr this page
            blob = page_rankings_bucket.blob(file_name.split('/')[-1])
            blob.name = file_name.split('/')[-1]
            blob.upload_from_string('0')
            return 'File uploaded to blob'
        else:
            return 'Ineligible filename'

    '''Uploads file to bucket 'wikicontent' as a blob if file_name exists.
        
        Returns:
            Strings corresponding to expected results for unit testing.
    '''

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

    '''Uploads file to bucket 'userpasswordinfo' as a blob containing userdata in the event of eligible user and password.
        
        Returns:
             Strings corresponding to expected results for unit testing.
    '''
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
            if user + '.txt' == blob.name:
                user_info = blob
                break

        if not user_info:
            return user_and_password_match

        user_and_password_match[0] = True
        check_password = None

        with user_info.open(mode='r') as file:
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
                with blob.open(mode='rb') as file:
                    image = base64.b64encode(file.read())
                break
        if not image:
            print('image not found')
            return None
        else:
            return image

    def load_all_page_rankings(self):
        '''Fetches all blobs from the pagerankings bucket in google cloud storage
        and stores them sorted by ranking.
        '''
        bucket = self.storage_client.get_bucket('pagerankings')
        blobs = bucket.list_blobs()
        self.page_rankings = []
        self.num_pages_to_show = 5
        for blob in blobs:
            with blob.open('r') as f:
                self.page_rankings.append((blob.name, int(f.read())))
        self.page_rankings.sort(key=lambda x: x[1])

    def get_page_rankings(self):
        '''Makes a copy of the first num_pages_to_show rankings.

        Returns:
            A list of tuples containing the name and the rank of a page.
        '''
        self.load_all_page_rankings()
        return [
            self.page_rankings[i][0]
            for i in range(-1, -self.num_pages_to_show, -1)
        ]

    def update_vote(self, page, user, vote):
        '''Updates the voting records and ranking for a page after a user votes.
        If a user's vote is the same as their current vote the method will exit.
        '''
        # update pagevoters
        bucket = self.storage_client.get_bucket('pagevoters')
        blob = bucket.get_blob(page)
        with blob.open('r') as f:
            page_voters = json.loads(f.read())
        if user in page_voters and page_voters[user] == vote:
            return
        page_voters[user] = vote
        blob.upload_from_string(json.dumps(page_voters))
        # update pagerankings
        bucket = self.storage_client.get_bucket('pagerankings')
        blob = bucket.get_blob(page)
        with blob.open('r') as f:
            blob.upload_from_string(str(int(f.read()) + vote))
