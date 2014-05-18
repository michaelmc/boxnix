from folders import Folders
import sys

TOKEN = ''

def main():
    if (len(sys.argv) != 5): 
        print "usage: boxnix.py <flags> <token> <Box file or location> <local file or location>"
        sys.exit()
    flags = sys.argv[1]
    folder = Folders(sys.argv[2])
    box = sys.argv[3]
    local = sys.argv[4]

    if 'u' in flags and 'd' in flags:
        print 'Only one of u or d can be used'
        return None
    elif 'u' in flags:
        folder.traverse(box)
        folder.upload(local)    
    elif 'd' in flags:
        folder.traverse(box, local)
    else:
        print 'Use the u or d flag to upload or download respectively'

if __name__ == '__main__':
    main()
