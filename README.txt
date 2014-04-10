1) python startUp_RunMe.py

2) hit 'ENTER'

3) cd /home/hcalpro/sckao/11_11_4/hcal/hcalUHTR

4) #Init and check links
bin/linux/x86_64_slc6/uHTRtool.exe 192.168.114.16
\n
LINK
INIT
1
6 #or 5
STATUS	# check if 'Align occ' and 'Align delta' are the SAME, STABLE (do 'STATUS' for a few times) and NONE ZERO for links that's 'ON'
QUIT
EXIT
EXIT

5) #Run auto run script
python run.py --nEvents 1000 --fName test.txt

#to spy on run
tail -f /home/hcalpro/sckao/11_11_4/hcal/hcalUHTR/run_log.txt

# python run.py -h # for all the possible options
