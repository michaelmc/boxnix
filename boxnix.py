import folders
import requests
import sys

TOKEN = ''

def main():
    if (len(sys.argv) != 2): 
        print "usage: boxnix.py <token>"
        sys.exit()
    TOKEN = sys.argv[1]

if __name__ == '__main__':
    main()
