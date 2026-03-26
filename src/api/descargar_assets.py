import requests
import os
import time
import re

API_KEY = "f4748b79d0a351345220d671c07880ff5ebb10bc"
HEADERS = {"User-Agent": "ProyectoAssetsMarvel_V3"}

def limpiar_nombre_final(nombre, es_comic=False):
    if not nombre: return "sin-nombre"
    
    # 1. Convertir a minúsculas
    nombre_limpio = nombre.lower()
    
    # 2. Quitar caracteres especiales (comillas, símbolos, puntuación)
    # Solo deja letras de la a-z y números del 0-9
    nombre_limpio = re.sub(r'[^a-z0-9\s]', '', nombre_limpio)
    
    # 3. Reemplazar espacios por guiones bajos (más seguro para Windows/Linux)
    nombre_limpio = nombre_limpio.strip().replace(" ", "_")
    
    # 4. Quitar guiones bajos repetidos (___ -> _)
    nombre_limpio = re.sub(r'_+', '_', nombre_limpio)
    
    # 5. Agregar el sufijo si es comic (opcional, según lo que pidió Mari)
    if es_comic:
        return f"{nombre_limpio}_comic"
    return nombre_limpio

def ejecutar_descargas():
    tareas = [
        ["characters", "assets/personajes", False],
        ["issues", "assets/comics", True]
    ]

    for endpoint, carpeta, es_comic in tareas:
        # Asegurar que la ruta sea correcta desde la raíz
        if not os.path.exists(carpeta): 
            os.makedirs(carpeta, exist_ok=True)
        
        print(f"\n--- 📦 Descargando y Limpiando {endpoint} ---")
        api_url = f"https://comicvine.gamespot.com/api/{endpoint}/?api_key={API_KEY}&format=json&limit=100"
        
        try:
            res = requests.get(api_url, headers=HEADERS)
            if res.status_code == 420:
                print("⚠️ Límite de API alcanzado. Esperando...")
                time.sleep(10)
                continue
            
            items = res.json().get('results', [])
            exitos = 0

            for item in items:
                # Obtener nombre original
                nombre_raw = item.get('name') if not es_comic else item.get('volume', {}).get('name')
                
                if not nombre_raw or not item.get('image'): 
                    continue

                # --- AQUÍ ESTÁ EL CAMBIO: Limpiamos antes de guardar ---
                nombre_limpio = limpiar_nombre_final(nombre_raw, es_comic=es_comic)
                ruta_final = os.path.join(carpeta, f"{nombre_limpio}.jpg")

                if os.path.exists(ruta_final):
                    exitos += 1
                    continue

                img_url = item['image'].get('medium_url')
                if not img_url: continue

                try:
                    img_res = requests.get(img_url, headers=HEADERS, timeout=10)
                    if img_res.status_code == 200:
                        with open(ruta_final, 'wb') as f:
                            f.write(img_res.content)
                        print(f"✅ Guardado limpio: {nombre_limpio}.jpg")
                        exitos += 1
                        time.sleep(0.5) 
                except Exception:
                    continue

            print(f"✔️ {endpoint} terminado: {exitos}/100 archivos limpios.")

        except Exception as e:
            print(f"💥 Error: {e}")

if __name__ == "__main__":
    ejecutar_descargas()