from urllib.request import urlopen 
from bs4 import BeautifulSoup 
import re

perfiles = []
html = urlopen('https://www.doctoralia.com.mx/buscar?q=&loc=San+Carlos')
bs = BeautifulSoup(html, 'html.parser')
#print(bs)
for link in bs.find('div').select("a.text-body"):
    if '/perfil/' in link.attrs['href']:
        perfiles.append(link.attrs['href'])
print(perfiles)