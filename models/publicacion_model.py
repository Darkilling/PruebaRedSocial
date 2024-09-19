class publicacion

    def __init__(self, id, likes, contenido, fecha_publicacion, usuario_id):
        self.id = id
        self.usuario_id = usuario_id
        self.contenido = contenido
        self.fecha_publicacion = fecha_publicacion
        self.likes = likes