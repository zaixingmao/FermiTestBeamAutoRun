#Tool to create the config string for QIE registers

import sys
import getopt

qie_default = { "lvds" : 0, "lvds_trim" : 2, "discon" : 0, "tgain" : 0, "ttdac" : 255, "tiref" : 0, "pdac" : 6, "capid0p" : 0, "capid1p" : 0, "capid2p" : 0, "capid3p" : 0, "fixrange" : 0, "rangeset" : 0, "cidac" : 0, "isetp" : 0, "idcset" : 0, "calmode" : 0 }

def mergeopts( default, opts ):
    for opt, arg in opts:
        optstr = opt[2:]
        if optstr in default:
            default[optstr] = int( arg )

def makereg( settings ):
    reg = 0L
    reg |= long( settings['lvds'] & 1 ) << 0
    reg |= long( settings['lvds_trim'] & 3 ) << 1
    reg |= long( settings['discon'] & 1 ) << 3
    reg |= long( settings['tgain'] & 1 ) << 4
    reg |= long( settings['ttdac'] & 255 ) << 5
    reg |= long( settings['tiref'] & 7 ) << 13
    if settings['pdac'] >= 0:
      reg |= long( settings['pdac'] & 31 ) << 16
      reg |= 1L << 21
    else:
      reg |= long( -settings['pdac'] & 31 ) << 16
    reg |= long( settings['capid0p'] & 15 ) << 22
    reg |= long( settings['capid1p'] & 15 ) << 26
    reg |= long( settings['capid2p'] & 15 ) << 30
    reg |= long( settings['capid3p'] & 15 ) << 34
    reg |= long( settings['fixrange'] & 1 ) << 38
    reg |= long( settings['rangeset'] & 3 ) << 39
    reg |= long( settings['cidac'] & 7 ) << 41
    reg |= long( settings['isetp'] & 31 ) << 44
    reg |= long( settings['idcset'] & 31 ) << 49
    reg |= long( settings['calmode'] & 1 ) << 54
    return reg

myargv='--pdac=10'

def main():
    qie_strlist = []
    for s in qie_default.keys():
        qie_strlist.append( s + '=' )
    #opts, args = getopt.getopt( myargv.split(), '', qie_strlist )
    opts, args = getopt.getopt( sys.argv[1:], '', qie_strlist )
    d = qie_default.copy()
    mergeopts( d, opts )
    reg = makereg( d )
    print "Register value:", hex( reg )
    for i in range( 8 ):
        print reg & 0xff,
        reg >>= 8

main()
