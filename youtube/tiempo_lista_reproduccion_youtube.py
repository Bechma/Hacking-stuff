from urllib.request import urlopen
import re

url = input("Introduce url del playlist a analizar: ")

try:
	with urlopen(url) as page:
		a = re.findall(">(\d+):(\d+)<", page.read().decode("utf-8"))

	min = sum([int(par[0]) for par in a])
	sec = sum([int(par[1]) for par in a])
	min += int(sec / 60)
	hour = int(min / 60)
	min %= 60
	sec %= 60

	print("{2} horas {0} minutos {1} segundos".format(min, sec, hour))
except Exception:
	print("playlist inválido, por favor, introduce un playlist correcto")
