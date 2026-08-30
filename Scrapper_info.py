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
            "clinicas": [
            {
                "nombre_clinica" : nombre,
                "telefonos" : [telefono 1, telefono 2]
                "google maps" : www.maps
            },
            {
                "nombre_clinica" : nombre2,
                "telefonos" : [telefono 1, telefono 2]
                "google maps" : www.maps
            }
            ]
        }
    }
"""
def info_scrapper():
    links = profile_scrapper([])
    doctors_json = {}

    for link in links:
        html = urlopen(link)
        bs = BeautifulSoup(html, 'html.parser')

        #Nombre
        nombre = bs.find(attrs={"data-test-id" : "doctor-header-fullname"}).get_text(strip = True)

        #clinicas
        #clinicas = [clinica.get_text(strip=True) for clinica in bs.find_all(attrs={"data-test-id": "address-info-name"})]
        clinicas = bs.find_all(attrs={"data-id" : "doctor-address-item"})
        clinicas_json = []
        for clinica in clinicas:
            nombre_tag = clinica.find(attrs={"data-test-id": "address-info-name"})
            nombre_clinica = nombre_tag.get_text(strip=True) if nombre_tag else "None"

            direccion_tag = clinica.find(attrs={"data-test-id": "address-info-street"})
            direccion = direccion_tag.get_text(strip=True) if direccion_tag else "None"

            maps = clinica.find('a', href=re.compile('/maps/'))
            maps_href = maps.attrs['href'] if maps else "None"

            telefonos = [telefono.get_text(strip=True) for telefono in clinica.find_all('b')]
            clinicas_json.append({
                "nombre clinica" : nombre_clinica,
                "direccion" : direccion, 
                "mapa" : maps_href, 
                "telefonos" : telefonos
                })
            
        print(clinicas_json)

    return()
info_scrapper()