#!/usr/bin/env python
import os as os
import optparse

def opts():
    parser = optparse.OptionParser()
    parser.add_option('--nEvents', dest='nevents', default='10', help='amount of events to be saved (DEFAULT=10)')
    parser.add_option('--fName', dest='fname', default='test.txt', help='name of output file (DEFAULT=test.txt)')
    parser.add_option('--fibers', dest='fibers', default='4', help='fibers to be saved, separate by \',\' (DEFAULT=4)')
    parser.add_option('--nBXbefore', dest='bxBefore', default='-15', help='BXs to store before trigger (DEFAULT=-15)')
    parser.add_option('--nBXafter', dest='bxAfter', default='25', help='BXs to store after trigger (DEFAULT=25)')
    options, args = parser.parse_args()
    return options

def checkSavingComplete(logFile, nEvents):
    logFileContent = open(logFile, 'r').readlines()
    key = 'read out event %i of %s \n' %(int(nEvents)-1, nEvents)
    if key in logFileContent:
        print 'Saving Complete :)'
    else:
        print 'Saving Incomplete :( Please check %s' %logFile



op = opts()

f = open('run.uhtr', 'w')

commandList = [' ', 'LINK', 'L1ACAPTURE', 'AUTORUN', op.nevents,
               '-15','25', '1', op.fibers, op.fname, 'QUIT', 'QUIT','EXIT','EXIT']
for i in commandList:
    f.write('%s\n'%i)
f.close()
currentDir = os.getcwd()
os.chdir('/home/hcalpro/sckao/11_11_4/hcal/hcalUHTR')
uHTR_command = 'bin/linux/x86_64_slc6/uHTRtool.exe 192.168.114.16 -s %s/run.uhtr > %s/run_log.txt' %(currentDir,currentDir)
print 'log file saved at: %s/run_log.txt' %currentDir
print 'starting to save %s events to %s ...' %(op.nevents, op.fname)
os.system(uHTR_command)

checkSavingComplete('%s/run_log.txt' %currentDir, op.nevents)
