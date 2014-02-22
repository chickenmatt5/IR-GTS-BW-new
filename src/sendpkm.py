#!/usr/bin/python

from pokehaxlib import *
from pkmlib import encode
from boxtoparty import makeparty
#from gbatonds import makends
from sys import argv, exit
from platform import system
from base64 import urlsafe_b64encode
from os import listdir
import os.path, gtsvar, hashlib

def sendpkm():

    print 'Note: you must exit the GTS before sending a pkm'
    print '4th Gen Pokemon files are currently unsupported.'
    print 'Enter the path or drag the pkm file here'
    print '(Type Back to go back)'

    while True:
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
        
    sendingpkm(path)

def multisend():

    print 'Note: you must exit the GTS before sending each Pokemon'
    print '4th Gen Pokemon files are currently unsupported.\n'
    print 'Enter the path or drag the pkm file here, then\npress Enter, and enter another path. Finish by typing\nDone then press Enter.'
    print '(Type Back to go back)'

    multi = list()

    while True:
        path = raw_input().strip()

        if path == "Back" or path == "back": return
        
        path = os.path.normpath(path)
        if system() != 'Windows':
            path = path.replace('\\', '')

        if path == 'done' or path == 'Done':
            multisender(multi)
            break

        if path.startswith('"') or path.startswith("'"):
            path = path[1:]
        if path.endswith('"') or path.endswith("'"):
            path = path[:-1]
        if os.path.exists(path) and path.lower().endswith('.pkm'):
            multi.append(path)
        else:
            print 'Invalid file name, try again'
            continue

def multisender(multi):

    multisize = len(multi)

    for pokes in multi:
        print '\nSending %s...' % pokes
        sendingpkm(pokes)
        multisize = multisize - 1
        if multisize >= 1:
            raw_input('\nPlease exit the GTS, then press Enter to send next Pokemon\n')
            continue
        elif multisize == 0:
            print '\nFinished sending\n'
            return


def queuesend():

    print 'Note: you must exit the GTS before sending each Pokemon'
    print '4th Gen Pokemon files are currently unsupported.\n'
    
    qpoke = listdir('queue')
    qpokef = list()
    
    for qpokes in qpoke:
        qpokes = 'queue/%s' % qpokes
        if os.path.exists(qpokes) and qpokes.lower().endswith('.pkm'): qpokesf.append(qpokes)

    qpokefsize = len(qpokef)

    for qpokesf in qpokef:
        print 'Sending %s...\n' % qpokesf
        sendingpkm(qpokes)
        qpokefsize = qpokefsize - 1
        if qpokefsize >= 1:
            raw_input('\nYou must exit the GTS before sending the next Pokemon.\nHit Enter when ready.')
            continue
        elif qpokefsize == 0:
            print '\nFinished sending\n'
            return


def customqueuesend():

    print 'Note: you must exit the GTS before sending each Pokemon'
    print '4th Gen Pokemon files are currently unsupported.\n'
    
    while True:
        print 'Enter the path of the queue folder, then hit Enter'
        print '(Type Back to go back)'
        folder = raw_input()

        if folder == "Back" or folder == "back": return
        
        print '\n'

        if os.path.exists(folder) == False:
            print 'Invalid folder, try again\n'
            continue
        elif os.path.exists(folder) == True:
            break

    qpoke = listdir(folder)
    qpokesf = list()
    
    for qpokes in qpoke:
        qpokes = '%s/%s' % (folder,qpokes)
        if os.path.exists(qpokes) and qpokes.lower().endswith('.pkm'): qpokesf.append(qpokes)

    qpokesfsize = len(qpokesf)

    for qpokes in qpokesf:
        print 'Sending %s...\n' % qpokes
        sendingpkm(qpokes)
        if qpokesfsize >= qpokesfsize - 1:
            raw_input('\nYou must exit the GTS before sending the next Pokemon.\nHit Enter when ready.')
            continue
        elif qpokesfsize == 0:
            print '\nFinished sending\n'
            return


def sendingpkm(path):       
    with open(path, 'rb') as f:
        pkm = f.read()

    # Adding extra 100 bytes of party data
    if len(pkm) != 220 and len(pkm) != 136:
        print 'Invalid filesize: %d bytes. Needs to be either 136 or 220 bytes.' % len(pkm)
        return
    if len(pkm) == 136:
        print 'Pokemon is in PC format; adding party information now... ',
        pkm = makeparty(pkm)
        print 'Done.'

    print 'Encoding!'
    bin = encode(pkm)

###
# Support for .3gpkm files. Currently unfinished.
###

#   elif path.lower().endswith('.3gpkm'):
#       print 'Converting GBA file to NDS format...',
#       with open(path, 'rb') as f:
#           pkm = f.read()
#
#       if len(pkm) != 80 and len(pkm) != 100:
#           print 'Invalid filesize.'
#           return
#       pkm = makends(pkm)
#       print 'done.'
#
#       print 'Encoding!'
#       bin = encode(pkm)

###
#
###

    # Adding GTS data to end of file
    print 'Adding GTS data... '
    bin += '\x00' * 16
    bin += pkm[0x08:0x0a] # id
    if ord(pkm[0x40]) & 0x04: bin += '\x03' # Gender
    else: bin += chr((ord(pkm[0x40]) & 2) + 1)
    bin += pkm[0x8c] # Level
    bin += '\x01\x00\x03\x00\x00\x00\x00\x00' # Requesting bulba, either, any
    bin += '\xdb\x07\x03\x0a\x00\x00\x00\x00' # Date deposited (10 Mar 2011)
    bin += '\xdb\x07\x03\x16\x01\x30\x00\x00' # Date traded (?)
    bin += pkm[0x00:0x04] # PID
    bin += pkm[0x0c:0x0e] # OT ID
    bin += pkm[0x0e:0x10] # OT Secret ID
    bin += pkm[0x68:0x78] # OT Name
    bin += '\xDB\x02' # Country, City
    bin += '\x46\x01\x15\x02' # Sprite, Exchanged (?), Version, Lang
    bin += '\x01\x00' # Unknown
    print 'Done.'

    sent = False
    response = ''

    print 'Ready to send; you can now enter the GTS.'
    while not sent:
        sock, req = getReq()
        a = req.action
        if len(req.getvars) == 1:
            sendResp(sock, gtsvar.token)
            continue
        elif a == 'info':
            response = '\x01\x00'
            print 'Connection established.'
        elif a == 'setProfile': response = '\x00' * 8
        elif a == 'post': response = '\x0c\x00'
        elif a == 'search': response = '\x01\x00'
        elif a == 'result': response = bin
        elif a == 'delete':
            response = '\x01\x00'
            sent = True

        m = hashlib.sha1()
        m.update(gtsvar.salt + urlsafe_b64encode(response) + gtsvar.salt)
        response += m.hexdigest()
        sendResp(sock, response)

    print 'Pokemon sent successfully.',
