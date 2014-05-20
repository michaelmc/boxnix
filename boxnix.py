#!/usr/bin/python

"""Boxnix.

Usage:
  boxnix.py (-u|-d [-s]) <token> <box_location> [<local_location>]

Options:
  -h --help     Show this screen.
  --version     Show version.
  -u            Upload
  -d            Download
  -s            Search

"""
from docopt import docopt
from boxfolders import Folders

def main(arguments):
    if not arguments.get('<local_location>'):
        arguments['<local_location>'] = './'
    if arguments.get('-u'):
        folder.traverse(arguments.get('<box_location>')
        return folder.upload(arguments.get('<local_location>')    
    elif arguments.get('-d') and not arguments.get('-s'):
        return folder.traverse(arguments.get('<box_location>'), arguments.get('<local_location'>))
    elif arguments.get('-s'):
        results = folder.search(argments.get('<box_location>')
        print "Enter the number of the file to download. n goes to the next page, b goes back, q quits."
        i = 0
        while True:
            for j in range(0, 15):
                k = j + (i * 15)
                if (k < len(results)):
                    print str(k + 1) + ': ' + results[k][2] + results[k][1]
                else: break
            typing = raw_input()
            if (typing.isdigit() and int(typing) < len(results)):
                return folder.download(results[int(typing) - 1][0], 
                    results[int(typing) - 1][1], local)
            elif (typing == 'n' and k < len(results) - 1):
                i += 1
            elif (typing == 'b' and i > 0):
                i -= 1
            elif (typing == 'q'):
                return None
    else:
        print 'Use the u, d, or s flag to upload, download, or search respectively'
        return None

if __name__ == '__main__':
    arguments = docopt(__doc__, version="Boxnix 0.1")
    main(arguments)
