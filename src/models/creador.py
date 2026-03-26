class Creador:
    def __init__(self, id, nombre, imagen):
        self.id = id
        self.nombre = nombre
        self.imagen = imagen

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "imagen": self.imagen
        }