class Comic:
    def __init__(self, id, titulo, descripcion, fecha, isbn, imagen):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha = fecha
        self.isbn = isbn
        self.imagen = imagen

        self.personajes = []
        self.creadores = []

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "fecha": self.fecha,
            "isbn": self.isbn,
            "imagen": self.imagen
        }