#!/usr/bin/python

# "A script that acts as the GTS, for sending and receiving pokemon between a
# retail cart and a PC. Credit goes to LordLandon and his sendpkm script, as
# well as the description of the GTS protocol from
# http://projectpokemon.org/wiki/GTS_protocol
#
# - Infinite Recursion"
#
# Resurrection of the Infinite Recursion pseudo-GTS script, now with 40% more
# infinite recursion! This is always a work in progress, started by Infinite
# Recursion and LordLandon, with some code borrowed from Pokecheck.org.
# 
# - chickenmatt5

from src import gtsvar
from src.pokehaxlib import initServ
from src.getpkm import getpkm
from src.sendpkm import sendpkm
from src.stats import statana
from src.pokecheck import *
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

while True:
    print '\nChoose:'
    print 'a - analyze pkm file'
    print 'o - continue to online mode'
    print 'q - quit\n'
    choice = raw_input().strip().lower()

    if choice.startswith('a'): statana()
    elif choice.startswith('o'):
        print '\nContinuing to online menu...\n\n'
        break
    elif choice.startswith('q'):
        print 'Quitting program'
        exit()
    else:
        print 'Invalid option, please try again.'
        continue
    
    print 'Returning to menu...\n'

initServ()
sleep(1)


done = False
while True:
    print '\nChoose an option:'
    print 's - send pkm file to game'
    print 'r - receive Pokemon from game'
    print 'm - receive multiple Pokemon from game'
    print 'a - analyze pkm file'
    print 'd - download and send a pkm from Pokecheck.org to game'
    print 'p - search Pokecheck.org for pkm file'
    print 'q - quit\n'
    option = raw_input().strip().lower()

    if option.startswith('s'): sendpkm()
    elif option.startswith('r'): getpkm()
    elif option.startswith('m'):
        print 'Press ctrl + c to return to main menu'
        while True:
            try: getpkm()
            except KeyboardInterrupt: break
    elif option.startswith('a'): statana()
    elif option.startswith('d'): pcdownload()
    elif option.startswith('p'): pcsearch()
    elif option.startswith('q'):
        print 'Quitting program'
        break
    else:
        print 'Invalid option, try again'
        continue

    print 'Returning to main menu...'