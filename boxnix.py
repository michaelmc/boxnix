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
    folder = Folders(arguments.get('<token>'))
    if arguments.get('-u'):
        folder.traverse(arguments.get('<box_location>'))
        return folder.upload(arguments.get('<local_location>'))
    elif arguments.get('-d') and not arguments.get('-s'):
        return folder.traverse(arguments.get('<box_location>'), 
            arguments.get('<local_location>'))
    elif arguments.get('-s'):
        results = folder.search(arguments.get('<box_location>'), offset = 0)
        print """Enter the number of the file to download. n goes to the next 
            page, b goes back, q quits."""
        i = 0
        while True:
            j = (15 * i) + 1
            for result in results:
                print str(j) + ': ' + result[2] + result[1]
                j += 1
            typing = raw_input()
            if (typing.isdigit() and int(typing) > (15 * i) and 
                    int(typing) <= 15 * (i + 1)):
                return folder.download(results[(int(typing) - 1) % 15][0], 
                    results[(int(typing) - 1) % 15][1],  
                    arguments.get('<local_location>'))
            elif (typing == 'n' and len(results) == 15):
                i += 1
                results = folder.search(arguments.get('<box_location',
                    offset = i))
            elif (typing == 'b' and i > 0):
                i -= 1
                results = folder.search(arguments.get('<box_location',
                    offset = i))
            elif (typing == 'q'):
                return None

if __name__ == '__main__':
    arguments = docopt(__doc__, version="Boxnix 0.1")
    main(arguments)
