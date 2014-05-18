import requests

class Folders:
    def __init__(self, token):
        self.token = token
        self.folders = []
        f = requests.get('https://api.box.com/2.0/folders/0/', headers = { 'Authorization': 'Bearer ' + token })
        if (f.status_code != 200): return None
        self.folders.append(f.json())
        self.current_folder = self.folders[-1]

    def path(self):
        s = ''
        for folder in self.folders:
            s += folder.get('name') + '/'
        return s

    def traverse(self, path, local=None):
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
        for entry in self.current_folder.get('item_collection').get('entries'):
            if (entry.get('name') == item):
                return entry.get('type')
        return None

    def list(self):
        item_dict = {}
        for entry in self.current_folder.get('item_collection').get('entries'):
            item_type = entry.get('type')
            if (item_type == 'folder' or item_type == 'file'):
                print entry.get('name') + ", " + item_type
                item_dict[entry.get('name')] = (entry.get('id'), item_type)
        return item_dict

    def down(self, child, destination=None):
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
            f = requests.get('https://api.box.com/2.0/folders/' + item_id + '/', headers = { 'Authorization': 'Bearer ' + self.token })
            if (f.status_code != 200): 
                print "Folder couldn't be opened"
                return False
            self.folders.append(f.json())
            self.current_folder = self.folders[-1]
        elif (item_type == 'file'):
            f = requests.get('https://api.box.com/2.0/files/' + item_id + '/content/', headers = { 'Authorization': 'Bearer ' + self.token })
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

    def up(self):
        if (self.current_folder == self.folders[0]):
            print "Already at All Files"
            return False
        else:
            self.folders.pop(-1)
            current_folder = self.folders[-1]
            return True

    def upload(self, filename):
        parent_id = self.current_folder.get('id')
        item_id = None
        for entry in self.current_folder.get('item_collection').get('entries'):
            if (entry.get('name') == filename and entry.get('type') == 'file'):
                item_id = entry.get('id')
                break
        if (item_id == None):
            f = requests.post('https://upload.box.com/api/2.0/files/content', headers = { 'Authorization': 'Bearer ' + self.token }, data = { 'filename': filename, 'parent_id':parent_id }, files = { filename: open(filename, 'rb')})
        else:
            f = requests.post('https://upload.box.com/api/2.0/files/' + item_id + '/content', headers = { 'Authorization': 'Bearer ' + self.token }, data = { 'filename': filename }, files = { filename: open(filename, 'rb')})
        if (f.status_code == 409):
            print "File upload caused a conflict"
            return False
        elif (f.status_code != 201):
            print "Problem uploading the file"
            return False
        else:
            print "File uploaded"
            return True
