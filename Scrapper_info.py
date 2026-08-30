from urllib.request import urlopen 
from bs4 import BeautifulSoup 
import re
from Scrapper_doctores import profile_scrapper


"""
    Doctors_json = {
        "doctor1": {
            "nombre": "nombre 1",
            "clinica": "clinica nombre"
        },
        "doctor2": {
            "nombre": "nombre 1",
            "clinica": "clinica nombre"
        }
    }
"""
def info_scrapper():
    links = profile_scrapper([])
    doctors_json = {}

    for link in links:

        #Nombre
        html = urlopen(link)
        bs = BeautifulSoup(html, 'html.parser')
        print(bs.find(attrs={"data-test-id" : "doctor-header-fullname"}).get_text(strip = True))

    return()
info_scrapper()