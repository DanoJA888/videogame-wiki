#TODO(Project 1): Implement Backend according to the requirements.

from google.cloud import storage
import base64
import hashlib
import json


class Backend:

    def __init__(self, storage_client=storage.Client()):
        self.storage_client = storage_client
        self.page_rankings = []
        self.num_pages_to_show = 5
        self.total_pages = 0
        self.pages_counted = False

    # Returns the requested page
    def get_wiki_page(self, name, user):
        '''Fetches blob from wikicontent bucket in google clous storage

        Args:
            name:
                The name of the blob to be fetched.

        Returns:
            The name of the blob, its contents as a string, and its voting ratio.
        '''
        wiki_content_bucket = self.storage_client.get_bucket('wikicontent')
        page_rankings_bucket = self.storage_client.get_bucket('pagerankings')
        page_voters_bucket = self.storage_client.get_bucket('pagevoters')

        if not (wiki_content_blob := wiki_content_bucket.get_blob(name)):
            return 'The page does not exist.'

        page_rankings_blob = page_rankings_bucket.get_blob(name)
        page_voters_blob = page_voters_bucket.get_blob(name)
        with wiki_content_blob.open('r') as f:
            content = f.read()
        with page_rankings_blob.open('r') as f:
            voting_ratio = int(f.read())
        with page_voters_blob.open('r') as f:
            page_voters = json.loads(f.read())

        current_user_vote = page_voters[user] if user in page_voters else 0
        return wiki_content_blob.name, content, voting_ratio, current_user_vote

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
        if not file_name:
            return 'Ineligible filename'
        page_name = file_name.split('/')[-1]
        # uploads page
        wiki_content_blob = wiki_content_bucket.blob(page_name)
        wiki_content_blob.name = page_name
        wiki_content_blob.upload_from_filename(file_name)
        # allows page voting records to be stored for this page
        page_voters_blob = page_voters_bucket.blob(page_name)
        page_voters_blob.name = page_name
        page_voters_blob.upload_from_string('{}')
        # allows page rank to be tracked for this page
        page_rankings_blob = page_rankings_bucket.blob(page_name)
        page_rankings_blob.name = page_name
        page_rankings_blob.upload_from_string('0')
        return 'File uploaded to blob'

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

    '''
    Function that adds a new comment to the comment section.
    I retireve the list from the bucket, since it can only store files i made the list a json string when storing,
    so i convert the string into a python list, append the new comment, convert it back to a json string and upload to bucket
    Return values: for unit tests: if it is successful, return list with new comment, else return empty list
    
    '''

    def make_comment(self, page_name, username, comment):
        bucket = self.storage_client.get_bucket('commentsection')
        if comment == '':
            return []
        cs_name = page_name.split('.')[0] + '.json'
        blob = bucket.get_blob(cs_name)
        comment_as_json = blob.download_as_text()
        comment_section = json.loads(comment_as_json)
        comment_section.append((username, comment))
        updated_cs = json.dumps(comment_section)
        blob.upload_from_string(updated_cs, content_type='application/json')
        return comment_section

    '''
    function that pulls the comment section of the respective page. Again, since I am using lists and cant store directly
    i am getting the json string and converting it back to a list and returning that. if it exists ill be returning a python list
    with the comments, else im not returning anything other than a fail message
    '''

    def get_section(self, name):
        bucket = self.storage_client.get_bucket('commentsection')
        cs_name = name.split('.')[0] + '.json'
        blob = bucket.get_blob(cs_name)
        if not blob:
            return 'Comment Section Not Found'
        comments_as_json = blob.download_as_text()
        comments = json.loads(comments_as_json)
        return comments

    '''
    function that creates a new comment section. Since buckets can't store python lists directly, converted the lists 
    into json strings and stored that in the bucket instead. In theory, if th eusers upload the pages, i should create a cs
    whenever a valid file is uploaded
    In pages.py, in the upload() function notice the if statement checking if the file is of html type
    '''

    def create_comment_section(self, name=None):
        if not name:
            return 'Could Not Create Comment Section'
        bucket = self.storage_client.get_bucket('commentsection')
        name_with_html = name.split('/')[-1]
        page_name = name_with_html.split('.')[0] + '.json'
        blob = bucket.blob(page_name)
        blob.upload_from_string('[]', content_type='application/json')
        return 'Comment Section Created'

    def get_page_rankings(self):
        '''Fetches all blobs from the pagerankings bucket in google cloud storage
        and stores them sorted by ranking.

            Returns:
                A list containing the names of the pages.
        '''
        bucket = self.storage_client.get_bucket('pagerankings')
        blobs = bucket.list_blobs()
        self.page_rankings = []
        # pulls ranking information from gcs and stores it as a list of tuples (pagename, voting_ratio)
        for blob in blobs:
            if not self.pages_counted:
                self.total_pages += 1
            with blob.open('r') as f:
                self.page_rankings.append((blob.name, int(f.read())))
        self.pages_counted = True
        # sorts page_rankings by voting ratio
        self.page_rankings.sort(key=lambda x: x[1], reverse=True)
        # returns only the names of the pages
        return [self.page_rankings[i][0] for i in range(self.num_pages_to_show)]

    def update_vote(self, page, user, new_vote):
        '''Updates the voting records and ranking for a page after a user votes.
        If a user's vote is the same as their current vote the method will exit.
        '''
        pagevoters_bucket = self.storage_client.get_bucket('pagevoters')
        pagerankings_bucket = self.storage_client.get_bucket('pagerankings')

        pagevoters_blob = pagevoters_bucket.get_blob(page)
        with pagevoters_blob.open('r') as f:
            page_voters = json.loads(f.read())
        current_vote = page_voters[user] if user in page_voters else 0
        duplicate_vote = current_vote == new_vote
        # update pagerankings
        pagerankings_blob = pagerankings_bucket.get_blob(page)
        with pagerankings_blob.open('r') as f:
            pagerankings_blob.upload_from_string(
                str(
                    int(f.read()) - current_vote +
                    (0 if duplicate_vote else new_vote)))
        # update pagevoters
        if duplicate_vote:
            new_vote = 0
        page_voters[user] = new_vote
        pagevoters_blob.upload_from_string(json.dumps(page_voters))

    '''
    function that loads more pages, edge case for when there are no more pages to load, for when you click to load more but
    there are less pages left to load than the amount added every time, and for when there is more pages after loading left
    '''

    def load_more_pages(self):
        if self.num_pages_to_show == self.total_pages:
            return 'No more pages to load'
        elif self.num_pages_to_show + 5 > self.total_pages:
            self.num_pages_to_show += (self.total_pages -
                                       self.num_pages_to_show)
            return 'loading final pages'
        else:
            self.num_pages_to_show += 5
            return 'loading more pages'
