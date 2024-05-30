import requests
import os
from dotenv import load_dotenv


def obtener_distancia(origen, destino, api_key):
    distance_matrix_url = (
        f"https://maps.googleapis.com/maps/api/distancematrix/json?"
        f"origins={origen['lat']},{origen['lng']}&"
        f"destinations={destino['lat']},{destino['lng']}&"
        f"key={api_key}"
    )

    response = requests.get(distance_matrix_url)
    data = response.json()

    if data['status'] != 'OK':
        raise Exception(f"Error en la solicitud a la API de Distance Matrix: {data['status']}")

    try:
        distancia_entre_lugares = data['rows'][0]['elements'][0]['distance']['text']
        tiempo_viaje = data['rows'][0]['elements'][0]['duration']['text']
    except (KeyError, IndexError):
        raise Exception("Error al extraer los datos de distancia y duración de la respuesta.")

    return distancia_entre_lugares, tiempo_viaje


if __name__ == '__main__':
    load_dotenv()
    apiKey = os.getenv('GOOGLE_API_KEY')
    lugar_origen = {'lat': -33.53751529253465, 'lng': -70.66434475541553}  # Metro La Cisterna
    lugar_destino = {'lat': -33.498587907748245, 'lng': -70.6134084324915}  # Campus San Joaquín

    distancia, duracion = obtener_distancia(lugar_origen, lugar_destino, apiKey)

    print(f"Distancia: {distancia}")
    '''print(f"Duración: {duracion}")'''
