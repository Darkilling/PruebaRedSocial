from models.publicacion_model import Publicacion

class PublicacionController:
    def __init__(self):
        self.publicaciones = []

    def agregar_publicacion(self, usuario_id, contenido, fecha):
        if len(contenido) > 500:
            raise ValueError("La publicación no puede exceder los 500 caracteres")

        nueva_publicacion = Publicacion(
            id=len(self.publicaciones) + 1,
            usuario_id=usuario_id,
            contenido=contenido,
            fecha=fecha
        )
        self.publicaciones.append(nueva_publicacion)

    def listar_publicaciones(self):
        return self.publicaciones
    

    




    '''def delete_client(self, id):
        self.clientes = [client for client in self.clientes if client.id != id]

    def update_client(self, id, nombre, email):
        for cliente in self.clientes:
            if cliente.id == id:
                cliente.nombre = nombre
                cliente.email = email
                return True
        return False'''