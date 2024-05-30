import requests
import os
from dotenv import load_dotenv

load_dotenv()

apiKey = os.getenv('GOOGLE_API_KEY')


def obtener_colegios_comuna(api_key, comuna):
    query = f"Colegios en {comuna}, Santiago, Chile"
    places_url = f'''https://maps.googleapis.com/maps/api/place/textsearch/json?query={query.replace(' ', '+')}
                    &key={api_key}'''

    lista_colegios = []
    next_page_token = None

    while True:
        if next_page_token:
            places_url = f'''https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={next_page_token}
                        &key={api_key}'''

        places_response = requests.get(places_url)
        places_data = places_response.json()

        if places_data['status'] != 'OK':
            raise Exception("Error obteniendo los colegios. Respuesta: " + str(places_data))

        for result in places_data['results']:
            nombre = result['name']
            direccion = result.get('formatted_address', 'Dirección no disponible')
            latitud = result['geometry']['location']['lat']
            longitud = result['geometry']['location']['lng']
            if comuna in direccion:
                if any(word in nombre.lower() for word in ["básica", "media", "liceo", "escuela", "colegio"]):
                    lista_colegios.append({
                        'nombre': nombre,
                        'direccion': direccion,
                        'latitud': latitud,
                        'longitud': longitud
                    })

        next_page_token = places_data.get('next_page_token', None)
        if not next_page_token:
            break
        else:
            import time
            time.sleep(3)

    return lista_colegios


if __name__ == '__main__':
    comuna_colegios = "Providencia"
    colegios = obtener_colegios_comuna(apiKey, comuna_colegios)

    contador = 0
    for colegio in colegios:
        contador += 1
        print(f'''Nombre: {colegio['nombre']}, Dirección: {colegio['direccion']}''')
        print(f'''Latitud: {colegio['latitud']}, Longitud: {colegio['longitud']}\n''')

    print("Cantidad Colegios:", contador)
