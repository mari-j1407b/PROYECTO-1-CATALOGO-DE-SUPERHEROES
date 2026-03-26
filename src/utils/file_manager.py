import json
import os

def cargar_datos(nombre_archivo):
    ruta = f"data/{nombre_archivo}.json"
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def obtener_datos_paginados(nombre_archivo, num_pagina, tamano_pagina=10):
    """
    Carga el JSON y devuelve solo los 100 elementos que corresponden a la página.
    """
    todos_los_datos = cargar_datos(nombre_archivo)
    inicio = (num_pagina - 1) * tamano_pagina
    fin = inicio + tamano_pagina
    
    return todos_los_datos[inicio:fin]