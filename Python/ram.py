#!/usr/bin/env python3.8

import time
import datetime
import psutil
import os

path = "/scripts/data"

now = datetime.datetime.now()
m = int((now.hour*60+now.minute)/5)
file = open(f"{path}/ram-{now.month}-{now.day}.txt", "a")
file.write(str(m)+" "+str(psutil.virtual_memory().available)+"\n")
if m == 1:
	for file in os.listdir(path):
		l = time.time() - os.path.getmtime(path+"/"+file)
		if l > 604800: # 60*60*24*7 = 604800
			os.remove(path+"/"+file)