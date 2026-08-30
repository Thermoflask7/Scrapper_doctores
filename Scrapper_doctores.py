from urllib.request import urlopen 
from bs4 import BeautifulSoup 
import re
#ligas de doctores
def profile_scrapper(perfiles):
    html = urlopen('https://www.doctoralia.com.mx/buscar?q=&loc=San+Carlos') #liga para extraer para x lugar
    bs = BeautifulSoup(html, 'html.parser')
    #print(bs)
    for link in bs.find('div').select("a.text-body"): 
        if '/perfil/' in link.attrs['href']:
            perfiles.append(link.attrs['href'])
    return(perfiles)