import requests

class Folders:
    def __init__(self, token):
        self.folders = []
        params = { 'offset': 0 }
        header = { 'Authorization': 'Bearer ' + token }
        f = requests.get('https://api.box.com/2.0/folders/0/items', params=params, headers=header)
        if (f.status_code != 200) return false
        self.folders.append(f)
