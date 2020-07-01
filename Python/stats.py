#!/usr/bin/env python3.8

import time
import datetime
import psutil
import os

path = "/data"

def zero(a):
	a = str(a)
	if(len(a)==1):
		return "0"+a
	else:
		return a

now = datetime.datetime.now()
m = int((now.hour*60+now.minute)/5)
data = []

data.append(str(m))
data.append(str(psutil.virtual_memory().used))
cpu = psutil.cpu_percent(5)
data.append(str(cpu))
file = open(f"{path}/{zero(now.month)}.{zero(now.day)}.txt", "a")
file.write(" ".join(data)+"\n")
file.close()
if m == 1:
	for file in os.listdir(path):
		l = time.time() - os.path.getmtime(path+"/"+file)
		if l > 604800: # 60*60*24*7 = 604800
			os.remove(path+"/"+file)