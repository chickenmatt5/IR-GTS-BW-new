from array import array
from namegen import namegen
from boxtoparty import makeparty, ivcheck, evcheck
from data import *
from platform import system
from datetime import datetime
import os, struct, sys

def statread(pkm, path):
    p = array('B')
    p.fromstring(pkm)

    s = statsetup(p, pkm, path)
    s += '\n'
    s += '=' * 80 + '\n\n'

    print 'Writing stats to statlog.txt... '
    with open('statlog.txt', 'a') as f:
        f.write(s)
    print 'Done.'

def statana():
    while True:
        print 'Enter .PKM file path'
        print '(Type Back to go back)'
        path = raw_input().strip()

        if path == 'Back' or path == 'back':
            return
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
    
    s = statsetup(p, pkm, path)

    print '\nBeginning analysis:\n'
    print s
	
    csum = struct.unpack('<6s1H', open(path, 'rb').read(8))[1]
    fcsum = struct.unpack(">I", struct.pack("<I", csum))[0]
    fcsum = ("%02x" % fcsum)[:-4]
    csum = struct.unpack(">I", struct.pack(">I", csum))[0]

    words = struct.unpack('<8s64H', open(path, 'rb').read(136))[1:]
    lilesum = sum(words) & 65535
    bigesum = struct.unpack(">I", struct.pack("<I", lilesum))[0]
    calcsum = ("%02x" % bigesum)[:-4]

    if lilesum != csum:
    	print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	print "File's checksum is incorrect(%s), should be %s." % (fcsum, calcsum)
	print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

    b = (p[0x38:0x3c])
    ivs = b[0] + (b[1] << 8) + (b[2] << 16) + (b[3] << 24)
    hp =  (ivs & 0x0000001f)
    atk = (ivs & 0x000003e0) >> 5
    df =  (ivs & 0x00007c00) >> 10
    spe = (ivs & 0x000f8000) >> 15
    spa = (ivs & 0x01f00000) >> 20
    spd = (ivs & 0x3e000000) >> 25
    total = hp + atk + df + spe + spa + spd
    if total == 186:
	print "\n! IVs are perfect, could be RNG abused or hacked. !"
    elif total >= 187:
        print "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	print "IVs are too high, none can exceed 31."
	print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

    evs = p[0x18:0x1e]
    total = evs[0] + evs[1] + evs[2] + evs[3] + evs[4] + evs[5]
    if total == 508:
	print "\n! Total EVs exactly 508. !"
    elif total == 510:
    	print "\n! Total EVs exactly 510. !"
    elif total >= 511:
	print "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	print "Total EVs over 510, too high."
	print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"


    if p[0x40] & 4:
    	gender = 0 #Genderless
    elif p[0x40] & 2:
	gender = 1 #Female
    else: gender = 2 #Male

    pid = struct.unpack('<0s4L', open(path, 'rb').read(16))[1]

    rgender = p[0x00]
    if rgender <= 128:
	cgender = 1 #Female
    if rgender >= 128:
	cgender = 2 #Male

    genratio = rgender / 2.56

    if gender != cgender and gender == 1:
	print "\n! Probably female, check gender ratio (file's ratio is %d%%). !" % (genratio)
    if gender != cgender and gender == 2:
	print "\n! Probably male, check gender ratio (file's ratio is %d%%). !" % (genratio)


    if p[0x5f] == 0:
    	print '\n!!!!!!!!!!!!!!!!!!!!!!!'
	print 'Game of origin not set.'
	print '!!!!!!!!!!!!!!!!!!!!!!!'
    elif p[0x5f] == 24 or p[0x5f] == 25:
        print '\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        print 'Game of origin too new (X/Y gen 6).'
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

    secid = (p[0x0f] << 8) + p[0x0e]
    if secid == 0: print "\n!!!!! Secret ID is 0 (could be an event). !!!!!"

    print '\n========End of analysis========\n'
	
    statread(pkm, path)

    print '\n'

def statsetup(p, pkm, path):
    pid = p[0x00] + (p[0x01] << 8) + (p[0x02] << 16) + (p[0x03] << 24)
    nickname = ''
    if p[0x49] != 0:
        nickname = 'Invalid nickname'
    else:
        for i in pkm[0x48:0x5e]:
            if i == '\xff': break
            if i != '\x00': nickname += i
    lv = p[0x8c]
    nat = natget(ord(pkm[0x41]))
    spec = specget((p[0x09] << 8) + p[0x08])
    dwabil = '(hidden/DW ability) ' if p[0x42] == 1 else ''
    abil = abiget(p[0x15])
    if p[0x40] & 4:
        gender = '(Genderless)'
    elif p[0x40] & 2:
        gender = '(Female)'
    else: gender = '(Male)'
    otname = ''
    if p[0x69] != 0:
        otname = 'TRAINER'
    else:
        for i in pkm[0x68:0x78]:
            if i == '\xff': break
            if i != '\x00': otname += i
    otid = (p[0x0d] << 8) + p[0x0c]
    secid = (p[0x0f] << 8) + p[0x0e]
    held = heldget((p[0x0b] << 8) + p[0x0a])
    ivs = ivcheck(p[0x38:0x3c])
    evs = evcheck(p[0x18:0x1e])
    atk = attackcheck(p[0x28:0x30])
    hidden = hiddenpower(ivs)
    happy = p[0x14]
    shiny = shinycheck(pid, otid, secid)
    if shiny: shiny = 'SHINY'
    else: shiny = ''
    origin = gorget(p[0x5f])
    timetaken = str(datetime.now())[:-7]

    s = '"%s" (%s from %s)\n    ' % (nickname, timetaken, path)
    s += 'Lv %d %s %s %s\n    ' % (lv, shiny, spec, gender)
    s += 'Nature: %s,  Ability: %s%s\n\n    ' % (nat, dwabil, abil)
    s += 'Game of origin: %7s, PID: %d\n    ' % (origin, pid)
    s += 'OT: %s,  ID: %05d,  Secret ID: %05d\n    ' % (otname, otid, secid)
    s += 'Holding: %s,  Happiness: %d\n    ' % (held, happy)
    s += 'Hidden Power: %s-type, %d Base Power\n\n    ' % hidden
    s += 'Attacks: %-12s %-12s\n             %-12s %-12s\n\n    ' % atk
    s += 'IVs: HP %3d, Atk %3d, Def %3d, SpA %3d, SpD %3d, Spe %3d\n    ' % ivs
    s += 'EVs: HP %3d, Atk %3d, Def %3d, SpA %3d, SpD %3d, Spe %3d, Total %d\n' % evs
    return s

def shinycheck(pid, otid, secid):
    pida = pid >> 16
    pidb = pid & 0xffff
    ids = otid ^ secid
    pids = pida ^ pidb
    return (ids ^ pids) < 8
