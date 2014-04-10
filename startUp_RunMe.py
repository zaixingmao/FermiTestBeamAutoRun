#!/Usr/bin/env python
import os as os
import subprocess as subprocess
import json


# check control hub
os.system('/opt/cactus/bin/controlhub_status > log.txt')
grep_command = "grep 'Control Hub is up' log.txt "
if os.system(grep_command) != 0:
    print 'Starting control hub, type password:'
    os.system('su -c \'/opt/cactus/bin/controlhub_start\'')

 
#configure TTT to take external clock
os.system('./externalClockTTT.sh | python ~hcalpro/seema/TTTSoftware/src/TTTtool.py')
 
# #make AMC13 distribute the clock
am13_command = 'AMC13Tool.exe -n 11 -x AMC13Com.txt > amc13_log.txt'
os.system(am13_command)
# 
#  
# #configure ngCCM to take external clock
currentDir = os.getcwd()
os.chdir('/home/hcalpro/GLIBtool_UVA/')

#print os.getcwd()
os.system('./GLIBtoolSetup > %s/log_GLIB.txt' %(currentDir))
os.chdir(currentDir)
 
os.chdir('/home/hcalpro/sckao/11_11_4/hcal/hcalUHTR')
uHTR_command = 'bin/linux/x86_64_slc6/uHTRtool.exe 192.168.114.16 -s %s/init.uhtr > %s/log.txt' %(currentDir,currentDir)
os.system(uHTR_command)
print 'cd /home/hcalpro/sckao/11_11_4/hcal/hcalUHTR\n'
print 'bin/linux/x86_64_slc6/uHTRtool.exe 192.168.114.16\n'

# 

