#!/usr/bin/python

# "A script that acts as the GTS, for sending and receiving pokemon between a
# retail cart and a PC. Credit goes to LordLandon and his sendpkm script, as
# well as the description of the GTS protocol from
# http://projectpokemon.org/wiki/GTS_protocol
#
# - Infinite Recursion"
#
# Resurrection of the Infinite Recursion pseudo-GTS script, now with 80% more
# infinite recursion! This is always a work in progress, started by Infinite
# Recursion and LordLandon, with some code borrowed from Pokecheck.org.
# 
# - chickenmatt5

from src import gtsvar
from src.pokehaxlib import initServ
from src.getpkm import getpkm
from src.sendpkm import sendpkm, multisend, queuesend, customqueuesend
from src.stats import statana
from src.gbatonds import threetofour
#from src.pokecheck import *
from platform import system
from sys import argv, exit
from time import sleep
import os

s = system()
if s == 'Darwin' or s == 'Linux':
    if os.getuid() != 0:
        print 'Program must be run as superuser. Enter your password below' + \
                ' if prompted.'
        os.system('sudo ' + argv[0] + ' root')
        exit(0)

print "\n",gtsvar.version,"\n"
if gtsvar.stable == 'no':
    print "==============================================="
    print "EXPERIMENTAL/UNSTABLE VERSION! MIGHT HAVE BUGS!"
    print "===============================================\n"

def convertmenu():
    while True:
        print '\nChoose a conversion option:'
        print '1 - convert 3rd gen Pokemon file to 4th gen .pkm'
        print '2 - convert 3rd gen Pokemon file to 5th gen .pkm'
        print '3 - convert 4th gen .pkm to 5th gen .pkm'
        print 'r - return to main menu'
        print 'q - quit'
        number = raw_input().strip().lower()

        if number.startswith('1'): threetofour()
        elif number.startswith('2'): threetofive()
        elif number.startswith('3'): fourtofive()
        elif number.startswith('r'): break
        elif number.startswith('q'):
            print 'Quitting program'
            exit()
        else:
            print 'Invalid option, try again'
            continue

        print 'Returning to conversion menu...'

while True:
    print '\nChoose:'
    print 'a - analyze pkm file'
    print 'o - continue to online mode'
    print 'c - convert .pkm files to newer gens'
    print 'q - quit\n'
    print '\nPlease type your option, and press Enter\n'
    choice = raw_input().strip().lower()

    if choice.startswith('a'): statana()
    elif choice.startswith('o'):
        print '\nContinuing to online menu...\n\n'
        break
    elif choice.startswith('c'): threetofour()
    elif choice.startswith('q'):
        print 'Quitting program'
        exit()
    else:
        print 'Invalid option, please try again.'
        continue
    
    print 'Returning to menu...\n'

initServ()
sleep(1)

def sendmenu():
    while True:
        print '\nChoose an option to send Pokemon:'
        print 'o - send one Pokemon to game'
        print 'm - choose & send multiple Pokemon to game'
        print 'f - send all Pokemon in queue folder'
        print 'c - choose folder full of Pokemon to send'
        #print 'd - download and send a pkm from Pokecheck.org to game'
        print 'r - return to main menu'
        print 'q - quit\n'
        print '\nPlease type your option, and press Enter\n'
        soption = raw_input().strip().lower()

        if soption.startswith('o'): sendpkm()
        elif soption.startswith('m'):multisend()
        elif soption.startswith('f'): queuesend()
        elif soption.startswith('c'): customqueuesend()
        #elif soption.startswith('d'): pcdownload()
        elif soption.startswith('r'): break
        elif soption.startswith('q'):
            print 'Quitting program'
            exit()
        else:
            print 'Invalid option, try again'
            continue

        print 'Returning to send menu...'


done = False
while True:
    print '\nChoose an option:'
    print 's - send pkm file to game'
    print 'r - receive Pokemon from game'
    print 'm - receive multiple Pokemon from game'
    print 'a - analyze pkm file'
    #print 'p - search Pokecheck.org for pkm file'
    print 'q - quit\n'
    print '\nPlease type your option, and press Enter\n'
    option = raw_input().strip().lower()

    if option.startswith('s'): sendmenu()
    elif option.startswith('r'): getpkm()
    elif option.startswith('m'):
        print 'Press ctrl + c to return to main menu'
        while True:
            try: getpkm()
            except KeyboardInterrupt: break
    elif option.startswith('a'): statana()
    #elif option.startswith('p'): pcsearch()
    elif option.startswith('q'):
        print 'Quitting program'
        exit()
    else:
        print 'Invalid option, try again'
        continue

    print 'Returning to main menu...'
