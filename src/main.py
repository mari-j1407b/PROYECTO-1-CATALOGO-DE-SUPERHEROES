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

        
        self.cargar_banners()
        
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

        # Estado inicial
        self.ui.stackedWidget.setCurrentIndex(1)
        self.actualizar_labels_personajes()
        self.actualizar_labels_comics()

    # --- BANNERS ---
    def cargar_banners(self):
        try:
            ruta_banner = os.path.join("assets", "img", "mundo comic.png")

            if os.path.exists(ruta_banner):
                pixmap = QPixmap(ruta_banner)

                if hasattr(self.ui, "label_9"):
                    self.ui.label_9.setPixmap(pixmap)
                    self.ui.label_9.setScaledContents(True)

                if hasattr(self.ui, "label_20"):
                    self.ui.label_20.setPixmap(pixmap)
                    self.ui.label_20.setScaledContents(True)
            else:
                print("⚠️ No se encontró mundo comic.png en assets/img")

        except Exception as e:
            print(f"Error cargando banner: {e}")

    # --- CARGA ---
    def cargar_datos_en_estructuras(self):
        try:
            ruta_p = 'data/personajes_locales.json'
            if os.path.exists(ruta_p):
                with open(ruta_p, 'r', encoding='utf-8') as f:
                    for p in json.load(f):
                        nombre = p.get('name', 'N/A')
                        img_name = nombre.lower().replace(" ", "-") + ".jpg"
                        
                        obj_p = Personaje(
                            p.get('id'),
                            nombre,
                            p.get('deck', 'Sin descripción'),
                            img_name
                        )
                        self.lista_personajes.insertar(obj_p)
        except Exception as e:
            print(f"Error cargando personajes: {e}")

        try:
            ruta_c = 'data/comics_locales.json'
            if os.path.exists(ruta_c):
                with open(ruta_c, 'r', encoding='utf-8') as f:
                    for c in json.load(f):
                        nombre_v = c.get('volume', {}).get('name', 'Cómic')
                        img_name = nombre_v.lower().replace(" ", "-") + "-comic.jpg"
                        
                        obj_c = Comic(
                            c.get('id'),
                            nombre_v,
                            c.get('deck', 'N/A'),
                            "2026",
                            "N/A",
                            img_name
                        )
                        self.lista_comics.insertar(obj_c)
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
        
        pagina_actual = sw.currentWidget()

        # 🔥 SOLO labels de cards
        labels_en_pantalla = [
            l for l in pagina_actual.findChildren(QLabel)
            if l.parent().findChild(QToolButton)
        ]

        labels_en_pantalla.sort(key=lambda x: x.objectName())

        self.llenar_datos(
            labels_en_pantalla,
            self.lista_comics,
            indice,
            "titulo",
            "comics"
        )

    def actualizar_labels_personajes(self):
        sw = self.ui.stackedWidget_3
        indice = sw.currentIndex()
        
        pagina_actual = sw.currentWidget()

        labels_en_pantalla = [
            l for l in pagina_actual.findChildren(QLabel)
            if l.parent().findChild(QToolButton)
        ]

        labels_en_pantalla.sort(key=lambda x: x.objectName())

        self.llenar_datos(
            labels_en_pantalla,
            self.lista_personajes,
            indice,
            "nombre",
            "personajes"
        )

    def llenar_datos(self, lista_labels, lista, num_pag, atributo, subcarpeta):
        try:
            puntero = lista.cabeza

            # Saltar páginas
            for _ in range(num_pag * 10):
                if puntero:
                    puntero = puntero.siguiente

            for label in lista_labels:
                contenedor = label.parent()
                boton = contenedor.findChild(QToolButton)
                
                if puntero:
                    texto = getattr(puntero.dato, atributo, "Sin Nombre")
                    imagen = getattr(puntero.dato, "imagen", "placeholder.jpg")

                    label.setText(f'"{texto}"')

                    ruta_imagen = os.path.join("assets", subcarpeta, imagen)

                    if boton:
                        if os.path.exists(ruta_imagen):
                            boton.setIcon(QIcon(ruta_imagen))
                        else:
                            boton.setIcon(QIcon())
                    
                    puntero = puntero.siguiente
                else:
                    label.setText("---")
                    if boton:
                        boton.setIcon(QIcon())

        except Exception as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MundoComic()
    ventana.show()
    sys.exit(app.exec())