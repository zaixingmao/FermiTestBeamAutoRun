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
    parser.add_option('--maxEvents', dest='maxEvents', default='10000', help='maximum events in a file (DEFAULT=10000)')
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
commandList = []
maxEvents = int(op.maxEvents)

if int(op.nevents) > maxEvents:
    print 'nEvent > %i, breaking output file into separate files ...' %maxEvents
for i in range(1, int(op.nevents)/maxEvents + 2):
    if i*maxEvents < int(op.nevents):
        nEventCurrent = maxEvents
    else:
        nEventCurrent = int(op.nevents) - (i-1)*maxEvents
    commandList.append((' ', 'LINK', 'L1ACAPTURE', 'AUTORUN', nEventCurrent, op.bxBefore, op.bxAfter, '0', op.fibers, op.fname[0:op.fname.rfind('.')]+'_%i.txt' %i, 'QUIT', 'QUIT','EXIT','EXIT'))


for i in range(len(commandList)):
    f = open('run%i.uhtr' %i, 'w')
    for j in commandList[i]:
        f.write('%s\n'%j)
    f.close()

currentDir = os.getcwd()
os.chdir('/home/hcalpro/sckao/11_11_4/hcal/hcalUHTR')

for i in range(len(commandList)):
    if (i+1)*maxEvents < int(op.nevents):
        nEventCurrent = maxEvents
    else:
        nEventCurrent = int(op.nevents) - i*maxEvents
    uHTR_command = 'bin/linux/x86_64_slc6/uHTRtool.exe 192.168.114.16 -s %s/run%i.uhtr > %s/run_log.txt' %(currentDir,i,currentDir)
    print 'log file saved at: %s/run_log.txt' %currentDir
    print 'starting to save %s events to %s ...' %(nEventCurrent, op.fname[0:op.fname.rfind('.')]+'_%i.txt' %(i+1))
    os.system(uHTR_command)
    if (i+1)*maxEvents < int(op.nevents):
        print 'saved %i out of %i ...' %((i+1)*maxEvents, int(op.nevents))
    else:
        print 'saving complete..'

#checkSavingComplete('%s/run_log.txt' %currentDir, op.nevents)
