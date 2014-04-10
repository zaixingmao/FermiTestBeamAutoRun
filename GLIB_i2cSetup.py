#!/usr/bin/env python

import os
import i2c_ctrl
import optparse


def getRegValues(line):
    regValues = []
    tmpCha = ''
    line.rstrip()
    for i in range(len(line)):
        if line[i] == ' ':
            regValues.append(tmpCha)
            tmpCha = ''
        if line[i] != '\n':
            tmpCha = tmpCha+line[i]
    regValues.append(tmpCha)
    return regValues

qie_default = {"lvds" : 0, "lvds_trim" : 2, "discon" : 0, "tgain" : 0,
               "ttdac" : 255, "tiref" : 0, "pdac" : 6, "capid0p" : 0,
               "capid1p" : 0, "capid2p" : 0, "capid3p" : 0, "fixrange" : 0,
               "rangeset" : 0, "cidac" : 0, "isetp" : 0, "idcset" : 0, "calmode" : 0}

runNicolosScript = 'python i2c_ctrl.py '

def opts():
    parser = optparse.OptionParser()
    for k, v in qie_default.items():
        parser.add_option('--%s' %k, dest=k, default=str(v), help='test')
    options, args = parser.parse_args()
    return options

op = opts()

colosScript = 'python i2c_ctrl.py'
for k, v in qie_default.items():
    runNicolosScript += ' --%s %s' %(k, getattr(op,k))
    os.system(runNicolosScript + ' > RegValues.txt')
commandLines = ['','GBT', 'NGCCM_IO', 'I2C_WRITE', '11', '50000', '0x10', '0x32']

linesInRegValues = open('RegValues.txt', 'r').readlines()
regValues = getRegValues(linesInRegValues[1])

printRegValues = ''
for i in range(6):
    for j in range(8):
        commandLines.append(regValues[j])             
        if i == 0:
            printRegValues = printRegValues + ' %s' %regValues[j]

commandLines.append('')
commandLines.append('SLOT_RD')
commandLines.append('11')
commandLines.append('50000')
commandLines.append('0x10')
commandLines.append('0x32')
commandLines.append('48')
commandLines.append('QUIT')
commandLines.append('QUIT')
commandLines.append('EXIT')
commandLines.append('EXIT')

currentDir = os.getcwd()
f = open('%s/i2cSetup.txt' %currentDir, 'w')

for i in commandLines:
    f.write('%s\n'%i)
f.close()

f2 = open('%s/GLIB_i2cSetup' %currentDir, 'w')
f2.write('#!/bin/bash\n')
f2.write('LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`pwd` IPBUS_MAP_PATH=`pwd` ./GLIBtool.exe -t ufec 192.168.0.111 < i2cSetup.txt')
f2.close()
os.system('chmod 777 GLIB_i2cSetup')

print '\nSetting values: %s' %printRegValues

os.system('./GLIB_i2cSetup > %s/log_GLIB.txt' %(currentDir))
