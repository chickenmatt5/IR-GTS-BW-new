from platform import system
from array import array
from webbrowser import open_new
from boxtoparty import makeparty
from sendpkm import sendingpkm
from time import sleep
import os, struct, urllib

def pcsearch():
    print '\nWill search Pokecheck.org for PID and level, might\nbe multiple results with different species.\n\n'
    while True:
        print 'Enter pkm file'
        print '(Type Back to go back)"
        path = raw_input().strip()

        if path == "Back" or path == "back": return
        
        path = os.path.normpath(path)
        if system() != 'Windows':
            path = path.replace('\\', '')

        if path.startswith('"') or path.startswith("'"):
            path = path[1:]
        if path.endswith('"') or path.endswith("'"):
            path = path[:-1]
        if os.path.exists(path) and path.lower().endswith('.pkm'): break
        else:
            print 'Invalid file name, try again'
            continue
        
    with open(path, 'rb') as f:
        pkm = f.read()

    if len(pkm) != 220 and len(pkm) != 136:
        print 'Invalid filesize: %d bytes. Needs to be either 136 or 220 bytes.' % len(pkm)
        return
    if len(pkm) == 136:
        print 'Pokemon is in PC format; adding party information now... ',
        pkm = makeparty(pkm)
        print 'Done.'
    p = array('B')
    p.fromstring(pkm)

    pid = hex(struct.unpack('<0s4L', open(path, 'rb').read(16))[1])[:-1]
    lvl = str(p[0x8c])

    print 'Opening new browser window with search results...'
    sleep(5)
    url = 'https://www.pokecheck.org/?p=search&pid=%s&lvf=1&lvl=%s' % (pid, lvl)
    open_new(url)

def pcdownload():
    print 'Enter the full URL of the Pokecheck Pokemon you want to upload'
    print '(Type Back to go back)'
    pcurl = raw_input()

    if pcurl == "Back" or pcurl == "back": return
    
    pcurl = '%s&export=Download+.pkm+file' % pcurl
    print '\nDownloading pkm as temp.pkm, will delete after upload.'

    if os.path.exists('temp.pkm'):
        print 'temp.pkm already exists, deleting...'
        os.remove("temp.pkm")
    
    urllib.urlretrieve(pcurl, "temp.pkm")
    print 'Download finished, onto encoding...\n'

    sendingpkm('temp.pkm')
    os.remove("temp.pkm")
