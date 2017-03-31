import requests
import re

url = input("Introduce el playlist a analizar: ")

try:
    pagina = requests.get(url).text

    a = re.findall("<span aria-label=\"(\d+) minutos, (\d+) segundos\">", pagina)

    min = sum([int(par[0]) for par in a])
    sec = sum([int(par[1]) for par in a])
    min += int(sec / 60)
    hour = int(min / 60)
    min %= 60
    sec %= 60

    print("{2} horas {0} minutos {1} segundos".format(min, sec, hour))
except Exception:
    print("playlist inválido, por favor, introduce un playlist correcto")