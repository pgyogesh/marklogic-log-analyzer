#!/usr/bin/env python
import re
import optparse
import datetime

parser = optparse.OptionParser() # To enable command line options
parser.add_option("-f","--file",dest="log_file",
                          action="store",help="Specify log file to be parsed")
options, args = parser.parse_args()
vLogFile=options.log_file

hour = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'] # To loop and check the log for every hour


def get_graph(log_type):
    counter = 0
    for h in hour:
        error_regex= '^^\d\d\d\d-\d\d-\d\d %s:\d\d:\d\d.\d\d\d %s:' %(h,log_type) #regex for error loge event
        file = open(vLogFile,"r")
        for line in file: #For loop to check the match in every line
            for match in re.finditer(error_regex,line,re.S):
                counter = counter + 1 # Increases the counter if match found
        if counter != 0:
            print("%s:%s:%s" %(h,counter * '*',counter)) # Prints the counter number of astericks if it is not equals to zero
        counter = 0 # Resets the counter
        file.close()

def get_custom():
    counter = 0
    custom_input = raw_input("Please enter string/regex to search in log=")
    for h in hour:
        custom_regex = '^\d\d\d\d-\d\d-\d\d %s:\d\d:\d\d.\d\d\d .*? %s' %(h,custom_input)
        file = open(vLogFile,"r")
        for line in file:
            for match in re.finditer(custom_regex,line,re.S):
                counter = counter + 1
        if counter != 0:
            print("%s:%s:%s" %(h,counter * '*',counter))
        counter = 0
        file.close()

def trim_log():
        start_time = raw_input("Please enter start time:\n[Format: HH:MM]=") # Takes start time as input
        end_time = raw_input("Please enter end time:\n[Format: HH:MM]=") # Takes end time as input
        trim_time = datetime.datetime.now().strftime('%d%H%M%S') # For the trimmied file name Ex. DDHHMMSS(DateHourMinuteSecond)
        output_file = 'trimmed_log_%s.txt' %trim_time # File name for trimmed log
        oFile = open(output_file, 'a')
        with open(vLogFile,'r') as input_file:
                do_write = False
                # Below block of code uses for loop to check every line with line numbers
                # Checks line number on to get date from line number 1
                # Sets True flag to write if start time found and sets False flag to write if end time found
                for i, line in enumerate(input_file, 1):
                        if i == 1:  # First line, so figure out the start/end markers
                                vDate = line[0:10]
                                start_line = vDate + ' ' + start_time
                                end_line = vDate + ' ' +end_time
                        if not do_write and line.startswith(start_line):  # If we need to start copying...
                                do_write = True
                                print('Starting to write from line %d' %i)
                        if do_write:
                                oFile.write(line)
                        if line.startswith(end_line):  # Stop writing, we have everything
                                print('Stopping write on line %d' %i)
                                break
        print("%s Created" %output_file)

if __name__ == '__main__':
    print("1. Error\n2. Warning\n3. Notice\n4. Critical\n5. Custom")
    vChoice = int(input("Please choose your option from above options (Ex. Choose 2 for Warnings)\n="))
    if vChoice == 1:
        get_graph('Error')
    elif vChoice == 2:
        get_graph('Warning')
    elif vChoice == 3:
        get_graph('Notice')
    elif vChoice == 4:
        get_graph('Critical')
    elif vChoice == 5:
        get_custom()
    else:
        print("Wrong input.. Exiting...!")
    trim_choice = raw_input("Do you want to trim error log:Yy|Nn[Default=N]\n=")
    if trim_choice == 'Y' or trim_choice == 'y':
        trim_log()
    else:
        print("Exiting on user request")
