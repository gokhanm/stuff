#!/usr/bin/env python3

__author__ = "Gokhan MANKARA <gokhan@mankara.org>"

import psutil
import os

def bytes2mb(n):
	return ( n / 1024 ) / 1024 

def disk_check(path):
	dsk = psutil.disk_usage(path)
	if dsk.percent >= 85:
		return "Warning"
def ram_check():
	mem = psutil.virtual_memory()
	mfree = bytes2mb(mem.free)
	if mfree < 1024:
		return "Warning"

def cpu_check():
	current = os.getloadavg()
	if current[0] > 10:
		return "Warning"

def status():
	returnVals = {}
	returnVals['DISK'] = disk_check('/')
	returnVals['RAM'] = ram_check()
	returnVals['CPU'] = cpu_check()
		
	if 'Warning' in list(returnVals.values()):
		for key, val in returnVals.items():
			if val == 'Warning':
				print("WARNING: {}".format(key))
	else:
		print("ALL GOOD")
			

if __name__ == "__main__":
    status()

