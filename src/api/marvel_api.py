import requests

API_KEY = "f4748b79d0a351345220d671c07880ff5ebb10bc"
BASE_URL = "https://comicvine.gamespot.com/api"
HEADERS = {"User-Agent": "MiProyectoMarvel"}

def obtener_comics():
    url = f"{BASE_URL}/issues/?api_key={API_KEY}&format=json&limit=100"
    res = requests.get(url, headers=HEADERS)
    return res.json()['results'] if res.status_code == 200 else []

def obtener_personajes():
    url = f"{BASE_URL}/characters/?api_key={API_KEY}&format=json&limit=100"
    res = requests.get(url, headers=HEADERS)
    return res.json()['results'] if res.status_code == 200 else []

def obtener_detalle_comic(comic_id):
    """Tarea: Descargar datos detallados de UN cómic"""
    url = f"{BASE_URL}/issue/4000-{comic_id}/?api_key={API_KEY}&format=json"
    res = requests.get(url, headers=HEADERS)
    return res.json()['results'] if res.status_code == 200 else {}

def obtener_eventos_personaje(personaje_id):
    """Tarea: Ver en qué 'eventos' (equipos) está un personaje"""
    url = f"{BASE_URL}/character/4005-{personaje_id}/?api_key={API_KEY}&format=json"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json()['results'].get('teams', [])
    return []
