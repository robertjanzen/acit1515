# apachelog5.py
#
# Read from an Apache access log
#
# Robert Janzen A01029341 1B

import sys
import os.path
import time
import operator

def read_file(file_name):
    file_list = []
    file = open(file_name, 'r')
    file_list = file.readlines()
    file.close()
    file_list = [line.rstrip() for line in file_list]
    print('Read successful\n')
    return file_list

def output_file(content):
    print('Last 10 lines')
    for line in content[-10:]:
        print(line)
    print('')
    return
        
def file_info(content,fname):
    print(len(content),'lines read from',fname,'\n')
    return
    
        
def commands():
    print('Available commands:' +
          '\n0. quit   -- Exit program' +
          '\n1. help   -- List availabe commands' +
          '\n2. read   -- Read the file' +
          '\n3. print  -- Show last 10 lines of file' +
          '\n4. info   -- File information' +
          '\n5. time   -- Parse date and time' +
          '\n6. error  -- All error codes' +
          '\n7. traffic - Show highest network traffic\n')
    return

def get_input():
    inp = ""
    while not inp:
        inp = input("Enter a command: ")
    return(inp.split())

def parse_time(content):
    first_line = content[0].split()
    last_line = content[-1].split()
    first_time = first_line[3]
    last_time = last_line[3]
    first = format_time(first_time)
    last = format_time(last_time)
    output = 'Logging started: %s %s, %s %s:%s %s\n' % (first[0], first[1], first[2], first[3], first[4], first[5])
    output += 'Logging finished: %s %s, %s %s:%s %s\n' % (last[0], last[1], last[2], last[3], last[4], last[5])
    return output

def format_time(time):
    date_list = []
    times = time.split(':')
    date_list.append(times[0][4:7])
    date_list.append(times[0][1:3])
    date_list.append(times[0][8:12])
    date_list.append(times[1])
    date_list.append(times[2])
    if int(times[1]) < 12:
        date_list.append('AM')
    else:
        date_list.append('PM')
    return date_list

def error_codes(content):
    error_list = []
    for line in content:
        errors = line.split()
        if errors[-2][0] == '4' or errors[-2][0] == '5':
            if errors[-2] not in error_list:
                error_list.append(errors[-2])
    return error_list

def traffic(content):
    servers = {}
    server_list = []
    index = -1
    
    # Add ip:byte information into a dictionary
    for line in content:
        server = line.split()
        if server[-2] == '200':
            
            # Add server and bytes dictionary if it doesn't already exist
            if server[0] not in servers:
                try:
                    int(server[-1])
                except ValueError:
                    continue
                servers[server[0]] = int(server[-1])
                
            # If it does exist, add bytes to the current value
            else:
                try:
                    int(server[-1])
                except ValueError:
                    continue
                servers[server[0]] += int(server[-1])
    
    # Turn dictionary into a list, then sort by the value
    server_list = [[k,v] for k, v in servers.items()]
    server_list.sort(key=lambda x: x[1])
    
    print('Server                                     Bytes')
    print('--------------------------------------  --------')
    for i in range(15):
        print('{0:38} {1:9}'.format(server_list[index][0],server_list[index][1]))
        index -= 1
    print('')
    return

def main():
    
    user_input = '-'
    
    # Check if the user has entered a file name
    if len(sys.argv) != 2:
        print('Usage: apachelog2.py input_file_name.txt')
        return
    else:
        # Check if the file exists
        if not os.path.isfile(sys.argv[1]):
            print('File',sys.argv[1],'does not exist')
            return
        
        # Ensure the file is a text file
        extension = sys.argv[1].split('.')
        if extension[1] != 'txt':
            print('Usage: apachelog2.py input_file_name.txt')
            return
        
    file_name = sys.argv[1]
    access_log = []
    commands()
    
    # Accept user commands
    while user_input != 'quit':
        if user_input == 'read':
            access_log = read_file(file_name)
        elif user_input == 'print':
            if not access_log:
                print('File not read\n')
            else:
                output_file(access_log)
        elif user_input == 'help':
            commands()
        elif user_input == 'info':
            if not access_log:
                print('File not read\n')
            else:
                file_info(access_log,file_name)
        elif user_input == 'time':
            if not access_log:
                print('File not read\n')
            else:
                print(parse_time(access_log))
        elif user_input == 'error':
            if not access_log:
                print('File not read\n')
            else:
                errors = error_codes(access_log)
                print('Error codes detected: ',end='')
                for item in errors:
                    print(item,' ',end='')
                print('\n')
        elif user_input == 'traffic':
            if not access_log:
                print('File not read\n')
            else:
                traffic(access_log)
            
        user_input = input('Enter a command (use [help] to list commands):')
    return
    
if __name__ == "__main__":
    main()