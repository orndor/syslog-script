#!/usr/bin/env python
# coding: utf-8

#This script parases through .txt Cisco IOS (firewall, routers, and switches) configurs a sub-directory called inputs
# and creates a .csv file which contains device hostname; loopback, fa0/0, or management vlan (222 or other), logging host, and logging level
#Folder struct will be as follows:
#*Folder: This script
#|-->inputs: .txt config files
#|-->outputs: outputs.csv

import glob
import os
os.chdir( "inputs" ) # go down one level into the inputs directory

interface = ''
with open('..\Output\output.csv',mode='w') as f: #open the output file in the outputs directory
    header = str('Device Name,Loopback IP,Logging Host,Trap Level\n') # create the header string to define each column
    f.write(header) # write it to the CSV file.
for file in glob.glob('*.txt'): # grab the next file in the 'inputs' directory
    with open (file) as in_file: # open the file
        with open('..\Output\output.csv',mode='a') as f: # open the output file again
            for line in in_file: # for each line in the file, check the following:
                if 'hostname' in line and 'stname context' not in line: # look for hostname but ignore in context exists
                    hostname = line[9::].rstrip('\r\n') # if true, just just the hostname and strip out word hostname
                if 'logging host' in line and '!' not in line and 'Add' not in line and 'trusted' not in line: # look for logging host but ignores comment lines
                    log_host = line[13::].rstrip('\r\n')
                if 'logging host untrusted' in line: # look for logging host in firewalls
                    log_host = line[23::].rstrip('\r\n')
                if 'logging host management' in line: # look for logging host in firewalls
                    log_host = line[24::].rstrip('\r\n')                
                if 'logging trap' in line: # look for logging level
                    log_trap = line[13::]
                while interface == '': # interface will be blank on the first run through.  if it matches on any line, it will ignore this while loop the next time through
                    if 'interface Loopback0' in line and '-' not in line: # look for loopback interfaces in routers
                        line = next(in_file)
                        interface = line[-32:27]
                        break # break out of where loop if there's a match
                    if 'interface FastEthernet0/0' in line: # look for fa0/0 interfaces in other devices, jump down two lines and grab the IP
                        line = next(in_file)
                        line = next(in_file)
                        interface = line[-32:27].rstrip('\r\n')
                        break # break out of where loop if there's a match
                    if 'interface Vlan222' in line: # look for vlan interfaces in other switches, jump down two lines and grab the IP
                        line = next(in_file)
                        line = next(in_file)
                        interface = line[-32:27].rstrip('\r\n')
                        break # break out of where loop if there's a match
                    if '! ip address ' in line: # look for management interfaces in firewalls, jump down a line and grab the IP
                        line = next(in_file)
                        interface = line[-32:26].rstrip('\r\n')
                    else: break # break out of where loop if there is not match, go back to top of for loop, and start with the next line in file.
            f.write(hostname + ',' + interface + ',' + log_host + ',' + log_trap) # write everything to a new line in the output.csv file
            interface = '' # set this blank for next for loop run through
            log_host = '' # set this blank for next for loop run through
            log_trap = '\n' # add a carriage return to nicely format the CSV file, should this be blank
