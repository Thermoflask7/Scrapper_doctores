from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
 
# ligas de doctores
def profile_scrapper(perfiles):
    req = Request(
        'https://www.doctoralia.com.mx/buscar?q=&loc=San+Carlos',  # liga para extraer para x lugar
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/120.0.0.0 Safari/537.36"
        }
    )
    html = urlopen(req)
    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.find('div').select("a.text-body"):
        if '/perfil/' in link.attrs['href']:
            perfiles.append(link.attrs['href'])
    return perfiles
 
