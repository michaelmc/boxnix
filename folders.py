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
        print s

    def list_contents(self):
        for entry in self.current_folder.get('item_collection').get('entries'):
            item_type = entry.get('type')
            if (item_type == 'folder' or item_type == 'file'):
                print entry.get('name') + ", " + item_type

    def down(self, child):
        item_id = None
        for entry in self.current_folder.get('item_collection').get('entries'):
            if (entry.get('name') == child):
                item_id = entry.get('id')
                item_type = entry.get('type')
                break
        if (item_id == None):
            print 'Requested item not found'
            return None

        if (item_type == 'folder'):
            f = requests.get('https://api.box.com/2.0/folders/' + item_id + '/', headers = { 'Authorization': 'Bearer ' + self.token })
            if (f.status_code != 200): 
                print "Folder couldn't be opened"
                return None
            self.folders.append(f.json())
            self.current_folder = self.folders[-1]
        elif (item_type == 'file'):
            f = requests.get('https://api.box.com/2.0/files/' + item_id + '/content/', headers = { 'Authorization': 'Bearer ' + self.token })
            if (f.status_code != 200): 
                print "File couldn't be opened"
                return None
            output = open(child, 'w')
            output.write(bytearray(f.content))
            output.close()

    def up(self):
        if (self.current_folder == self.folders[0]):
            print "Already at All Files"
        else:
            self.folders.pop(-1)
            current_folder = self.folders[-1]
