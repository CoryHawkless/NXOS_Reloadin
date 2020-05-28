#!/isan/bin/python

# Written by Ryan Tischer @ Cisco -  @ryantischer
# Designed to run on Nexus 9000 swtich
# script replicates IOS "reload in" command to schedule reloads
# leverages scheduler feature in NXOS

#Usage - 

#copy/save script in bootflash/scripts folder on swtich
#from NXOS CLI type "source reloadin.py [options]
#options...
#	- number of minutes until reload
#	- "save" to save configuration before reload.  Must be used as second option behine minutes
#	- "cancel" cancel reload
#Examples
# source reloadin.py 20 - schedules a reload in 20 minutes
# source reloadin.py 20 save - schedules a reload in 20 minutes and saves the config
# source reloadin.py cancel - cancels current reloadin command.  

# Possiable issue - 
# I have no idea what will happen with a day change...for example if the current time is 11:55 and 
# the reloadin.py 20 is issued.  It could work, it could break, it could form a blackhole.




#!/isan/bin/python

import datetime
from cli import cli
import sys

numArg = len(sys.argv)

# check if cancel

if sys.argv[1] == "cancel":

        schedCLIjob = 'conf t ; no scheduler job name reloadinCommand5657373'
        schedCLItime = 'conf t ; no scheduler schedule name reloadinCommand5657373'
        print "Canceling reload"
        exit()
        
# check number of argvs and if first one is an integer

elif numArg <= 3:
        try:

                requestTime = int(sys.argv[1])
        except:
                print "Enter a integer for time"
                sys.exit() #bail out if input is wrong

        now = datetime.datetime.now()
        actionTime = now + datetime.timedelta(minutes = requestTime)
        reloadTime = str(actionTime)
        reloadTime=reloadTime[11:-10]
        schedCLIjob =  'conf t ; no scheduler job name reloadinJob5657373 ; scheduler job name reloadinJob5657373 ; reload force ; exit'
        schedCLItime = 'conf t ; no scheduler schedule name reloadinSchedule5657373 ; scheduler schedule name reloadinSchedule5657373 ; job name reloadinJob5657373 ; time start ' + reloadTime + ' ; exit '

        if numArg == 3 and sys.argv[2] == "save".lower():
                cli('copy running-config startup-config')
                print "Saving config before reload"

        print "current time on the switch is " + str(now)
        print "reload scheduled at " + reloadTime

        # run the CLI
        cli('conf t ; feature scheduler')
        
        try:
                print("Running command " + schedCLIjob)
                cli(schedCLIjob)
        except:
                print "schedCLIjob operation failed"
                sys.exit()
        
                
        try:
                print("Running command " + schedCLItime)
                cli(schedCLItime)
        except:
                print "schedCLItime operation failed"
                sys.exit()
                
        
        print "Operation success"


