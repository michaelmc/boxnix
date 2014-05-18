import requests

class Folders:
    def __init__(self, token):
        """
        Initializer for the Folders class. Takes a bearer token as input and
        sets the root folder of the object to be the user's 'All Files' Box
        folder.

        Returns False if there is a problem communicating with Box, else True.
        """
        self.token = token
        self.folders = []
        f = requests.get('https://api.box.com/2.0/folders/0/', 
            headers = { 'Authorization': 'Bearer ' + token })
        self.folders.append(f.json())
        self.current_folder = self.folders[-1]

    def path(self):
        """
        Returns the current path of the Folder object in normal /-delimited
        form.
        """
        s = '/'
        for folder in self.folders:
            s += folder.get('name') + '/'
        return s

    def traverse(self, path, local=None):
        """
        Traverses a relative or absolute path from the Box 'All Files' root.
        
        Returns True if the entire path can be traversed, and False otherwise.
        """
        path = path.split('/')
        if (path[0] == ''):
            self.folders = [self.folders[0]]
            self.current_folder = self.folders[0] 
        if (path[1] == 'All Files'):
            path = path[2:]
        else:
            path = path[1:]
        for item in path:
            if (item != path[-1] and self.item_type(item) == 'file'):
                print 'Invalid path: file "' + item + '" found'
                return False
            elif (item != ''):
                if local == None:
                    self.down(item)
                else:
                    self.down(item, local)
                return True
            else:
                return False

    def item_type(self, item):
        """Returns the type of a specified item."""
        for entry in self.current_folder.get('item_collection').get('entries'):
            if (entry.get('name') == item):
                return entry.get('type')
        return None

    def list(self):
        """
        Lists out the file and folder contents of the current folder.

        Returns a dict with filenames as keys and tuples of file id and file
        type as the values.
        """
        item_dict = {}
        for entry in self.current_folder.get('item_collection').get('entries'):
            item_type = entry.get('type')
            if (item_type == 'folder' or item_type == 'file'):
                print entry.get('name') + ", " + item_type
                item_dict[entry.get('name')] = (entry.get('id'), item_type)
        return item_dict

    def down(self, child, destination=None):
        """
        Moves down one level. If the specified child is a folder, that becomes
        the new current folder. If the child is a file, that file is
        downloaded. The destination to which the file is downloaded is an
        optional argument.

        Returns True if the specified file or folder is reached, False
        otherwise.
        """
        item_id = None
        for entry in self.current_folder.get('item_collection').get('entries'):
            if (entry.get('name') == child):
                item_id = entry.get('id')
                item_type = entry.get('type')
                break
        if (item_id == None):
            print 'Requested item not found'
            return False
        if (item_type == 'folder'):
            f = requests.get('https://api.box.com/2.0/folders/' + item_id + '/',
                headers = { 'Authorization': 'Bearer ' + self.token })
            if (f.status_code != 200): 
                print "Folder couldn't be opened"
                return False
            self.folders.append(f.json())
            self.current_folder = self.folders[-1]
        elif (item_type == 'file'):
            f = requests.get('https://api.box.com/2.0/files/' + item_id + '/content/',
                headers = { 'Authorization': 'Bearer ' + self.token })
            if (f.status_code != 200): 
                print "File couldn't be opened"
                return False
            try:
                if (destination == None):
                    output = open(child, 'w')
                elif (destination.endswith('/')):
                    output = open(destination + child, 'w')
                else:
                    output = open(destination, 'w')
                output.write(bytearray(f.content))
                output.close()
                return True
            except IOError:
                print "File couldn't be saved"
                return False
        else:
            print "Requested item not a file or folder"
            return False

    def download(self, target, filename, destination=None):
        """
        Downloads a specified file by Box ID. The destination to which the file is downloaded is an
        optional argument.

        Returns True if the specified file or folder is reached, False
        otherwise.
        """
        f = requests.get('https://api.box.com/2.0/files/' + target + '/content/',
            headers = { 'Authorization': 'Bearer ' + self.token })
        if (f.status_code != 200): 
            print "File couldn't be downloaded"
            return False
        try:
            if (destination == None):
                output = open(filename, 'w')
            elif (destination.endswith('/')):
                output = open(destination + filename, 'w')
            else:
                output = open(destination, 'w')
            output.write(bytearray(f.content))
            output.close()
            return True
        except IOError:
            print "File couldn't be saved"
            return False
    
    def up(self):
        """
        Moves current folder up one level from present.

        Returns True if successful, False if the at the top already.
        """
        if (self.current_folder == self.folders[0]):
            print "Already at All Files"
            return False
        else:
            self.folders.pop(-1)
            current_folder = self.folders[-1]
            return True

    def upload(self, path):
        """
        Uploads a file to the current folder. Takes a file location as an
        argument, either relative or absolute. If a file of the same name is
        already in the current folder, a new version is uploaded.

        Returns True if file upload is successful, False otherwise.
        """
        parent_id = self.current_folder.get('id')
        item_id = None
        filename = path.split('/')[-1]
        for entry in self.current_folder.get('item_collection').get('entries'):
            if (entry.get('name') == filename and entry.get('type') == 'file'):
                item_id = entry.get('id')
                break
        if (item_id == None):
            f = requests.post('https://upload.box.com/api/2.0/files/content', headers = { 'Authorization': 'Bearer ' + self.token }, data = { 'filename': filename, 'parent_id':parent_id }, files = { filename: open(path, 'rb')})
        else:
            f = requests.post('https://upload.box.com/api/2.0/files/' + item_id + '/content', headers = { 'Authorization': 'Bearer ' + self.token }, data = { 'filename': filename }, files = { filename: open(path, 'rb')})
        if (f.status_code == 409):
            print "File upload caused a conflict"
            return False
        elif (f.status_code != 201):
            print "Problem uploading the file"
            return False
        else:
            print "File uploaded"
            return True

    def search(self, target):
        """
        Searches a user's Box account for a file based on a query string; 
        search looks both in filenames and in file contents and gets the 
        first 200 matching values. 

        Returns matching files as a list of tuples containing file ID, 
        filename, and Box path.
        """
        f = requests.get('https://api.box.com/2.0/search', params = { 'query': target, 'scope': 'user_content', 'type': 'file', 'limit': 200, 'offset': 0 }, headers = { 'Authorization': 'Bearer ' + self.token })
        if (f.status_code != 200):
            print "Error in search"
            return None 
        elif (f.json().get('total_count') > 0):
            files = []
            for item in f.json().get('entries'):
                path = '/'
                for parent in item.get('path_collection').get('entries'):
                    path += parent.get('name') + '/'
                files.append((item.get('id'), item.get('name'), path))
            return files
        else:
            print "Item not found"
            return None 
