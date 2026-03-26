class Personaje:
    def __init__(self, id, nombre, descripcion, imagen):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.imagen = imagen

        self.creadores = []
        self.comics = []
        self.eventos = []

    def agregar_creador(self, creador):
        self.creadores.append(creador)

    def agregar_comic(self, comic):
        self.comics.append(comic)

    def agregar_evento(self, evento):
        self.eventos.append(evento)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "imagen": self.imagen
        }