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

        #Especialidades FALTA CHECAR
        especialidad = bs.find(attrs={"data-test-id" : "doctor-specializations"}).get_text(strip = True) #imprime texto que no va

        #Experiencia
        experiencia = bs.find(attrs={"id" : "about-section"})
        if experiencia:
            formacion_tag = experiencia.find_all(attrs={"id" : "school"})
            formacion = [tag.get_text(strip=True) for tag in formacion_tag] if formacion_tag else "None"

            sobre_mi_tag = experiencia.find(attrs={"class": "about-content"})
            sobre_mi = sobre_mi_tag.get_text(strip=True) if sobre_mi_tag else "None"

            enfermedades_tratadas = [enfermedad.get_text(strip = True) for enfermedad in experiencia.find_all(attrs={"id" : "disease"})]

            idiomas = [lenguaje.get_text(strip = True) for lenguaje in experiencia.find_all(attrs={"id" : "language"})] #los idiomas salen como un string pegado

            enfoques = [enfoque.get_text(strip = True) for enfoque in experiencia.find_all(attrs={"id" : "expertIn"})] #los enfoques salen pegados como un solo string

            pacientes = experiencia.find_all(string=[re.compile('Adultos'), re.compile('Niños')]) #TDBN por ahora

            tipos_consulta = experiencia.find_all('Presencial', 'Videoconsulta') #NO FUNCIONA ACTUALMENTE

            redes_sociales = [red_social.attrs['href'] for red_social in experiencia.find_all(attrs={"rel" : "nofollow noopener noreferrer"})] #funciona pero tiene // al comienzo
    

            experiencia_json = {
                "formacion" : formacion,
                "sobre_mi" : sobre_mi, 
                "enfermedades_tratadas" : enfermedades_tratadas, 
                "idiomas" : idiomas,
                "enfoques" : enfoques,
                "pacientes" : pacientes
                }
        else: #No se si sea lo más correcto asumirque por que no hay experiencia entonces no hay nada de lo demas CHECAR
            experiencia_json = {
                "formacion" : "None",
                "sobre_mi" : "None", 
                "enfermedades_tratadas" : "None", 
                "idiomas" : "None",
                "enfoques" : "None",
                "pacientes" : "None"
                }

    return()
info_scrapper()