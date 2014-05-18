boxnix
======

A Python command line client for Box.

boxnix is still in the *very* early stages of development. Functionality is limited right now to the Folders class, which allows you, using an OAuth 2.0 or Box developer bearer token, to create Folders objects, traverse folders in Box, and download files.

Using boxnix
------------

Getting started:
```python
>>> from folders import Folders
>>> f = Folders('<bearer token>')
```

This gives you a Folders object that holds information about your Box account. Other available methods include:
* `f.path()` Prints the current path, starting from All Files in your Box account
* `f.list()` Lists contents of your current folder
* `f.up()` Goes up one level
* `f.down('<file or folder name>')` Goes down one folder or downloads a file
* `f.upload('<filename>')` Uploads a file to the current folder. If the file already exists (matched by name), a new version is uploaded

```python
>>> f.path()
All Files/
>>> f.list()
foo, folder
bar, folder
simon.txt, file
garfunkel.txt, file
>>> f.down('foo')
>>> f.list()
hall.txt, file
oates.txt, file
>>> f.path()
All Files/foo/
>>> f.up()
>>> f.path()
All Files/
>>> f.down('garfunkel.txt') # downloads the file to the current folder
>>> f.upload('crosby.txt')
```

Future development
------------------
In the short term, features planned for boxnix include: 
* A robustly-featured UI for end-user command line use, with autocomplete
* Uploading and versioning abilities
* Password authentication and secure storage of bearer tokens
