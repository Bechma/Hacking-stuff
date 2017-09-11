from bs4 import BeautifulSoup
from urllib import request


def contiene(item, vector):
	for ar in vector:
		if item in ar or ar in item:
			return False
	return True

# Esta url puede ser cambiada por la de cualquier otro periodico
url = "http://www.eldiario.es"
pagina = request.urlopen(url).read()
soup = BeautifulSoup(pagina, "html.parser")

articulos = []
contador = 0

for article in soup.find_all('article'):
	for div in article.find_all('a'):
		div = div.get('href')
		if div[0] == '/':
			div = url + div
		if div[0:len(url)] == url and contiene(div, articulos):
			articulos.append(div)
			contador += 1
			print(div)
if "http://www.elmundo.es/comunidad-valenciana/2017/09/11/59b59bc0268e3e5a5e8b45cc.html" in articulos:
	print("Esta aqui :D")
print(contador)
