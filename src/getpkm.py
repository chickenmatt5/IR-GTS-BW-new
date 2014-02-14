#!/usr/bin/python

# A simple script to copy pokemon from retail carts to a computer via GTS.
# Heavily relies on the sendpkm script and the description of the GTS protocol
# from http://projectpokemon.org/wiki/GTS_protocol
#
# --Infinite Recursion

from pokehaxlib import *
from pkmlib import decode
from sys import argv, exit
from base64 import urlsafe_b64decode, urlsafe_b64encode
from array import array
from stats import statread
import os.path, subprocess, platform, hashlib, gtsvar

def makepkm(bytes):
    ar = array('B') # Byte array to hold encrypted data
    ar.fromstring(bytes)

    ar = ar[12:232].tostring()
    pkm = decode(ar)

    return pkm

def save(path, data):
    saved = False

    while not saved:
        fullpath = os.path.normpath('Pokemon' + os.sep + path)
        saved = True
        if os.path.isfile(fullpath):
            print '%s already exists! Delete?' % path
            response = raw_input().lower()
            if response != 'y' and response != 'yes':
                print 'Enter new filename: (press enter to cancel save) '
                path = raw_input()
                if path == '':
                    print 'Not saved.',
                    return
                if not path.strip().lower().endswith('.pkm'):
                    path += '.pkm'
                saved = False

    with open(fullpath, 'wb') as f:
        f.write(data)

    print '%s saved successfully.\nYou should have received error 13266.' % path,

def getpkm():
    sent = False
    response = ''
    print 'Ready to receive from game.'
    while not sent:
        sock, req = getReq()
        a = req.action

        if len(req.getvars) == 1:
            sendResp(sock, gtsvar.token)
            continue
        elif a == 'info':
            response = '\x01\x00'
            print 'Connection Established.'
        elif a == 'setProfile': response = '\x00' * 8
        elif a == 'result': response = '\x05\x00'
        elif a == 'delete': response = '\x01\x00'
        elif a == 'search': response = '\x01\x00'
        elif a == 'post':
            response = '\x0c\x00'
            print 'Receiving Pokemon...'
            data = req.getvars['data']
            bytes = urlsafe_b64decode(data)
            decrypt = makepkm(bytes)
            filename = ''
            if decrypt[0x49] != '\x00':
                pid = 0
                for i in xrange(0, 4):
                    pid += ord(decrypt[i]) << (i * 8)
                filename = str(pid)
            else:
                for i in decrypt[0x48:0x5e]:
                    if i == '\xff':
                        break
                    if i != '\x00':
                        filename += i
            filename += '.pkm'
            save(filename, decrypt)
            cpath = 'in-game, saved to %s' % filename
            statread(decrypt, cpath)
            sent = True

        m = hashlib.sha1()
        m.update(gtsvar.salt + urlsafe_b64encode(response) + gtsvar.salt)
        response += m.hexdigest()
        sendResp(sock, response)
