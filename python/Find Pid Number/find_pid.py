#!/usr/bin/env python

from subprocess import Popen, PIPE
from re import split
from sys import stdout, argv, exit

__author__ = "Gokhan MANKARA"
__email__ = "gokhan@mankara.org"

class Proc(object):
    ''' Data structure for a processes . The class properties are
    process attributes '''
    def __init__(self, proc_info):

        self.pid = proc_info[1]

        self.cmd = proc_info[10]

    def to_dict(self):
        ''' Returns a string containing minimalistic info
        about the process : user, pid, and command '''
        proc_dict = {
                      "pid": self.pid,
                      "name": self.cmd
                    }
 
        
        return proc_dict

def get_proc_list():
    ''' Retrieves a list [] of Proc objects representing the active
    process list list '''
    proc_list = []
    sub_proc = Popen(['ps', 'aux'], shell=False, stdout=PIPE)
    #Discard the first line (ps aux header)
    sub_proc.stdout.readline()
    for line in sub_proc.stdout:
        #The separator for splitting is 'variable number of spaces'
        proc_info = split(" *", line.strip())
        proc_list.append(Proc(proc_info))
    return proc_list

if __name__ == "__main__":
    proc_list = get_proc_list()
    process_status = []

    if len(argv) == 1:
        print "Usage: find_pid.py process_name"
        exit(1)

    process_name = argv[1]

    for proc in proc_list:
        if process_name in proc.to_dict()['name']:
           process_status.append(True)
           pid = proc.to_dict()['pid']
           print "Process Name: %s Pid Number: %s" % (process_name, pid)
        else:
            process_status.append(False)

    if any(process_status) is False:
        print "Process %s NOT FOUND" % process_name

