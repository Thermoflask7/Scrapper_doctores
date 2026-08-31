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
        especialidad_tag = bs.find(attrs={"data-test-id" : "doctor-specializations"}) #imprime texto que no va
        especialidad = especialidad_tag.find('a'). get_text(strip=True) if especialidad_tag else "None"

        #Experiencia
        experiencia = bs.find(attrs={"id" : "about-section"})
        if experiencia:
            formacion_tag = experiencia.find_all(attrs={"id" : "school"})
            formacion = [tag.get_text(strip=True) for tag in formacion_tag] if formacion_tag else "None"

            sobre_mi_tag = experiencia.find(attrs={"class": "about-content"})
            sobre_mi = sobre_mi_tag.get_text(strip=True) if sobre_mi_tag else "None"

            enfermedades_tag = experiencia.find(attrs={"id" : "disease"})
            enfermedades_tratadas = [enfermedad.get_text(strip = True) for enfermedad in enfermedades_tag if enfermedad.get_text(strip=True)]  if enfermedades_tag else "None"

            lenguajes_tag  = experiencia.find(attrs={"id" : "language"})
            lenguajes = [lenguaje.get_text(strip = True) for lenguaje in lenguajes_tag if lenguaje.get_text(strip=True)] if lenguajes_tag else "None"

            enfoques_tag = experiencia.find(attrs={"id" : "expertIn"})
            enfoques = [enfoque.get_text(strip = True) for enfoque in enfoques_tag if enfoque.get_text(strip=True)] if enfoques_tag else "None" 

            # se puede hacer de una mejor forma seleccionando los iconos que aparentemente siempre vienen con cada tipo y moverse al texto de forma manual que es un span siguiente
            pacientes = experiencia.find_all(string=[re.compile('Adultos'), re.compile('Niños') ])

            # #NO FUNCIONA ACTUALMENTE, la mejor forma probablemente es seleccionar los iconos que aparentemente siempre vienen con cada tipo y moverse al texto de forma manual
            #tipos_consulta = experiencia.find(attrs={}) 
    
            redes_sociales = [red_social.attrs['href'] for red_social in experiencia.find_all(attrs={"rel" : "nofollow noopener noreferrer"})]

            experiencia_json = {
                "formacion" : formacion,
                "sobre_mi" : sobre_mi, 
                "enfermedades_tratadas" : enfermedades_tratadas, 
                "lenguajes" : lenguajes,
                "enfoques" : enfoques,
                "pacientes" : pacientes
                }
        else: #No se si sea lo más correcto asumir que por que no hay experiencia entonces no hay nada de lo demas CHECAR
            experiencia_json = {
                "formacion" : "None",
                "sobre_mi" : "None", 
                "enfermedades_tratadas" : "None", 
                "idiomas" : "None",
                "enfoques" : "None",
                "pacientes" : "None"
                }
        #print(experiencia_json)
        #print (redes_sociales)
        #print(especialidad) Hola mundo

        #No. de cedula
        cedula= bs.find(string = [re.compile('cédula:')])
        cedula=cedula.split(':')[-1].split() if cedula else "None"
        #re.sub(r"\s+", "", cedula) if cedula else None

 
        #aseguradoras
        #aseguradoras_tag= bs.find_all('li', attrs={"class" : "insurance-item"})
        #aseguradoras = [tag.get_text(strip = True) for tag in aseguradoras_tag] 
        #print(aseguradoras)


        opiniones_dest = bs.find_all('div', attrs={"data-test-id": "opinion-block"})
        opiniones_estan= bs.find_all(attrs={"class" : "standars-opinion-containers"})
        opiniones_tag = opiniones_dest + opiniones_estan
        opinion_json = []
        for opinion in opiniones_dest:

            #Nombre
            nombre = opinion.find('h4').get_text(strip=True)
            #print(nombre)

            #Estrellas
            estrellas = opinion.find('div', attrs={"class" : "rating"}).get('data-score')
            #print(estrellas)

            #Descripcion
            descripcion = opinion.find('p', attrs= {"data-test-id" : "opinion-comment"}).get_text(strip=True)
            #print(descripcion)

            #Fecha
            fecha = opinion.find('time').get_text(strip=True)
            #print(fecha)

            #lugar y procedimiento
            time_tag = opinion.find('time')
            span_container = time_tag.find_next_sibling('span', class_='small text-muted') if time_tag else None

            if span_container:
                textos = [c.strip() for c in span_container.contents if isinstance(c, str) and c.strip()]
                lugar = textos[0] if len(textos) > 0 else "None"
                procedimiento = textos[1] if len(textos) > 1 else "None"
            else:
                lugar = "None"
                procedimiento = "None"

            #print(lugar)
            #print(procedimiento)
            
            opinion_json.append({
                "nombre opinion" : nombre,
                "estrellas" : estrellas, 
                "comentario" : descripcion, 
                "fecha" : fecha,
                "lugar" : lugar,
                "procedimiento" : procedimiento
                })
    return() 
info_scrapper()