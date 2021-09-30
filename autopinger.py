#!/usr/bin/python3

#Author: Daniel Dumouchel
#Version: 1           

import subprocess
import csv
import os
import glob
import pandas as pd
from io import StringIO
import io
import socket
import numpy as np
import sys
import socket

### Rows to make adjustments to, for your personal use case
# 25  --> set your base directory
# 29 or 231  --> choose auto grab csv, or you input the csv name upon execution of script
# 119  --> selects your hostname column from your csv
# 194 --> optional if you want to delete your basdir and input file for full cleanup

########################################################################################################################################################
                                    ## UPDATE BASEDIR AND RAW_FILE TO YOUR SELECTED LOCATIONS AND SOURCE FILE ##
########################################################################################################################################################

basedir = "C:\"  #Put your base working directory here, so you only have to name this once
raw_file = "\something.something"  #name your starting file here... this file can be a major data dump, as long as "column B" has the hostnames --> you can use the other raw_file if you want to manually type in the source file at each execution... just comment out this one to switch it over
workdir = basedir + '\ping'  #this will put together the working directory for all results going forward
#raw_file = input("Enter the input file name: \\")  # Comment out other raw_file if you want to manually specify the file.... you must type out the file exactly as it is in your dir
########################################################################################################################################################
                        ## END SETUP STAGE. YOU MAY CONTINUE EDITING ON LINE 100, IF WANTED. THE SCRIPT IT READY AT THIS POINT ##
########################################################################################################################################################

########################################################################################################################################################
                                    ## DONT CHANGE ANYTHING UNTIL THE END OF THIS COMMENT SECTION ##
########################################################################################################################################################

def ping(host):
    p = subprocess.Popen('ping ' + host, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    pingStatus = 'ok';
            
    for line in p.stdout:
        output = line.rstrip().decode('UTF-8')
     
        if (output.endswith('unreachable.')) :
                #No route from the local system. Packets sent were never put on the wire.
            pingStatus = 'unreacheable'
            break
        elif (output.startswith('Ping request could not find host')) :
            pingStatus = 'host_not_found'
            break
        if (output.startswith('Request timed out.')) :
                #No Echo Reply messages were received within the default time of 1 second.
            pingStatus = 'timed_out'
            break
            #end if
        #endFor
        
    return pingStatus
    #endDef    


def printPingResult(host):
    statusOfPing = ping(host)
        
    if (statusOfPing == 'host_not_found') :
        writeToFile('ping_results.csv', host)
    elif (statusOfPing == 'unreacheable') :
        writeToFile('ping_results.csv', host)
    elif (statusOfPing == 'timed_out') :
        writeToFile('ping_results.csv', host)	
    elif (statusOfPing == 'ok') :
        writeToFile('ping_results.csv', host)
        #endIf
    #endPing


def writeToFile(filename, data) :
    with open(filename, 'a') as output:
        output.write(data + '\n')
        #endWith
    #endDef    
    
def create_file(folder_name, name, ext):
    import datetime
    d = datetime.datetime.today()
    d_formatdate = d.strftime('%m-%d-%Y-%I-%M-%S')
    filename = folder_name + "\\" + name + "_" + d_formatdate + "_." + ext
    import os
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    f = open(filename, "x")
    f.close()
    return filename

    '''
    servers.txt example
       vm8558
       host2
       server873
       google.com
      '''
########################################################################################################################################################
                                                ## YOU MAY NOW START EDITIING STUFF BELOW HERE ##
########################################################################################################################################################

    #create directory for ping results and find starting file
user = 'Log Host'
ping_results = create_file("ping", "ping_results", "csv") # where the results will go --> Creates a dir called "ping" and a csv called "ping_results"
# the below will look for a big data dump from the console and put its name/path into memory#
list_of_files = glob.glob(basedir + raw_file) # * means all if need specific format then *.csv
start_file = max(list_of_files) #gives file a name to work with as an object#
print(start_file)
    #grab start file and only grab hostnames
try:
        read = pd.read_csv(start_file, usecols=[1])  #the column with your hostnames is the column to use. Col 0 = Column A, 1=ColB, 2=ColC, etc... this default to ColB
        print(read)
        df = read.dropna()
        print(df)
        df.to_csv(workdir + '\hostnames.csv', index=False)  #removes only hostnames from the start file to start the automated manipulation#

finally:
        pass #close the file
        
    ##Find new file for pings    
list_of_files = glob.glob(workdir + '\hostnames.csv') # * means all if need specific format then *.csv
file = max(list_of_files)
print(file)
    

name = {}
CI = {}
host = {}
status = {}

try:

    with open(file, 'r', newline='') as csvinput:
        reader = csv.DictReader(csvinput)

        for rows in reader:
            CI = rows['Log Host']
            try:
                ip = socket.gethostbyname(CI)
            except socket.error:
                pass
            name = socket.getfqdn(CI)
            data = name

            host = rows['Log Host']
            response = subprocess.Popen(['ping.exe',host], stdout = subprocess.PIPE).communicate()[0]
            response = response.decode()
            print(response)
            if 'bytes=32' in response:
                status = 'Up'  ##name as you wish##
            elif 'destination host unreachable' in response:
                status = 'Unreachable'
            else:
                status = 'Down'  ##name as you wish##
            if status == 'Down':
                ip = 'Not Found'  ##name as you wish##
                
            ## puts results in below file ##
            with open(workdir + '\ping_results.csv', 'a', newline='') as csvoutput:
                output = csv.writer(csvoutput)
                output.writerow([host] + [data] + [status] + [ip])


            print("IP Lookup.......Finished")  
    print("Script.......Finished")  
finally:
        pass
        ###combine two docs into one useable doc##
list_of_files = glob.glob(workdir + '\ping_results_*.csv') # * means all if need specific format then *.csv
complete_file = max(list_of_files)
print(complete_file)

try:

    pdr = pd.read_csv(workdir + '\ping_results.csv')
    dffinal = pd.DataFrame(
         np.row_stack([pdr.columns, pdr.values]),
             columns=['host', 'servername', 'status', 'ip'])
    print(dffinal)
    
    
    outfile = dffinal.to_csv(complete_file, index=False)
    print(complete_file + "    you can find all your data in this file" + "\n \n" + "bye")
    os.remove(workdir + '\ping_results.csv')  #cleaning up no-longer needed files
    os.remove(workdir + '\hostnames.csv')     #cleaning up no-longer needed files
#    os.remove(basedir + raw_file)     #cleaning up no-longer needed files  --> This is if you want to remove your source file for any reason
    #endTry
finally:
    sys.exit(0) # exiing with a zero value is what we want for successful operations
