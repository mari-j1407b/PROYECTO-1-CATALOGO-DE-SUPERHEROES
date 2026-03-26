import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QToolButton
from PyQt6.QtGui import QIcon, QPixmap
from ui.Ui_interfaz import Ui_ventanaPrincipal 
from models.comic import Comic
from models.personaje import Personaje
from structures.lista_doble import ListaDoble

# Configuración de rutas
ruta_del_archivo = os.path.abspath(__file__)
directorio_src = os.path.dirname(ruta_del_archivo)
proyecto_raiz = os.path.dirname(directorio_src)
os.chdir(proyecto_raiz)

class MundoComic(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ventanaPrincipal() 
        self.ui.setupUi(self)
        
        print("\n--- BOTONES REALES EN LA INTERFAZ ---")
        for b in self.findChildren(QToolButton):
            print(b.objectName())
        
        self.lista_comics = ListaDoble()
        self.lista_personajes = ListaDoble()
        
        self.cargar_datos_en_estructuras()
        
        # Conexiones
        self.ui.btn_comics.clicked.connect(self.mostrar_seccion_comics)
        self.ui.btn_personajes.clicked.connect(self.mostrar_seccion_personajes)

        self.ui.btn_sig_comics.clicked.connect(self.cambiar_pag_comics_sig)
        self.ui.btn_ant_comics.clicked.connect(self.cambiar_pag_comics_ant)

        self.ui.btn_sig_personajes.clicked.connect(self.cambiar_pag_personajes_sig)
        self.ui.btn_ant_personajes.clicked.connect(self.cambiar_pag_personajes_ant)
        # Conexiones de busqueda
        self.ui.stackedWidget.setCurrentIndex(1) # Ir a Personajes
        self.actualizar_labels_personajes()
        self.actualizar_labels_comics()

    # --- CARGA ---
    def cargar_datos_en_estructuras(self):
        # 1. CARGAR PERSONAJES
        try:
            ruta_p = 'data/personajes_locales.json'
            if os.path.exists(ruta_p):
                with open(ruta_p, 'r', encoding='utf-8') as f:
                    for p in json.load(f):
                        nombre = p.get('name', 'N/A')
                        # Regla Mari: minúsculas y guiones
                        img_name = nombre.lower().replace(" ", "-") + ".jpg"
                        
                        obj_p = Personaje(p.get('id'), nombre, p.get('deck', 'Sin descripción'), img_name)
                        self.lista_personajes.insertar(obj_p)
            print(f"✅ Cargados {self.lista_personajes.longitud} personajes.")
        except Exception as e:
            print(f"Error cargando personajes: {e}")

        try:
            ruta_c = 'data/comics_locales.json'
            if os.path.exists(ruta_c):
                with open(ruta_c, 'r', encoding='utf-8') as f:
                    for c in json.load(f):
                        # En cómics el nombre suele venir en volume -> name
                        nombre_v = c.get('volume', {}).get('name', 'Cómic')
                        # Regla Mari: minúsculas, guiones y sufijo -comic
                        img_name = nombre_v.lower().replace(" ", "-") + "-comic.jpg"
                        
                        obj_c = Comic(c.get('id'), nombre_v, c.get('deck', 'N/A'), "2026", "N/A", img_name)
                        self.lista_comics.insertar(obj_c)
            print(f"✅ Cargados {self.lista_comics.longitud} cómics.")
        except Exception as e:
            print(f"Error cargando cómics: {e}")

    # --- NAVEGACIÓN ---
    def mostrar_seccion_comics(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.actualizar_labels_comics()

    def mostrar_seccion_personajes(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.actualizar_labels_personajes()

    def cambiar_pag_comics_sig(self):
        sw = self.ui.stackedWidget_2
        if sw.currentIndex() < sw.count() - 1:
            sw.setCurrentIndex(sw.currentIndex() + 1)
            self.actualizar_labels_comics()

    def cambiar_pag_comics_ant(self):
        sw = self.ui.stackedWidget_2
        if sw.currentIndex() > 0:
            sw.setCurrentIndex(sw.currentIndex() - 1)
            self.actualizar_labels_comics()

    def cambiar_pag_personajes_sig(self):
        sw = self.ui.stackedWidget_3
        if sw.currentIndex() < sw.count() - 1:
            sw.setCurrentIndex(sw.currentIndex() + 1)
            self.actualizar_labels_personajes()

    def cambiar_pag_personajes_ant(self):
        sw = self.ui.stackedWidget_3
        if sw.currentIndex() > 0:
            sw.setCurrentIndex(sw.currentIndex() - 1)
            self.actualizar_labels_personajes()

    # --- RENDER ---
    def actualizar_labels_comics(self):
        sw = self.ui.stackedWidget_2
        indice = sw.currentIndex()
        
        # Esto busca TODOS los labels que estén en la página que se ve ahorita
        pagina_actual = sw.currentWidget()
        labels_en_pantalla = pagina_actual.findChildren(QLabel)
        
        # Los ordenamos por nombre para que no se revuelvan (label_1, label_2...)
        labels_en_pantalla.sort(key=lambda x: x.objectName())

        self.llenar_datos(labels_en_pantalla, self.lista_comics, indice, "titulo", "comics")

    def actualizar_labels_personajes(self):
        sw = self.ui.stackedWidget_3
        indice = sw.currentIndex()
        
        pagina_actual = sw.currentWidget()
        labels_en_pantalla = pagina_actual.findChildren(QLabel)
        
        labels_en_pantalla.sort(key=lambda x: x.objectName())

        self.llenar_datos(labels_en_pantalla, self.lista_personajes, indice, "nombre", "personajes")



    def llenar_datos(self, lista_labels, lista, num_pag, atributo, subcarpeta):
        try:
            puntero = lista.cabeza
            
            # 1. Contar cuántos datos hay realmente (Verificación)
            total = 0
            temp = lista.cabeza
            while temp:
                total += 1
                temp = temp.siguiente
            print(f"DEBUG: Tienes {total} elementos en la lista de {subcarpeta}")

            # 2. Saltar a la página correcta
            for _ in range(num_pag * 10):
                if puntero: 
                    puntero = puntero.siguiente

            # 3. Llenar los labels
            for i, label in enumerate(lista_labels):
                # Verificamos que el contenedor tenga un botón
                contenedor = label.parent()
                boton = contenedor.findChild(QToolButton)
                
                if puntero:
                    texto = getattr(puntero.dato, atributo, "Sin Nombre")
                    imagen = getattr(puntero.dato, "imagen", "placeholder.png")
                    label.setText(f'"{texto}"')

                    # Construimos la ruta
                    ruta_imagen = os.path.join("assets", subcarpeta, imagen)

                    if boton:
                        if os.path.exists(ruta_imagen):
                            boton.setIcon(QIcon(ruta_imagen))
                        else:
                            print(f"DEBUG: No hallé la foto: {ruta_imagen}")
                            # Si tienes un placeholder, úsalo; si no, limpia el icono
                            boton.setIcon(QIcon()) 
                    
                    puntero = puntero.siguiente
                else:
                    # Limpiar si ya no hay más personajes
                    label.setText("---")
                    if boton:
                        boton.setIcon(QIcon())

        except Exception as e:
            print(f"¡ERROR CRÍTICO en llenar_datos!: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MundoComic()
    ventana.show()
    sys.exit(app.exec())