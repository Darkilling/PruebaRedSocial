from models.publicacion_model import Publicacion
from datetime import datetime

class PublicacionController:
    def __init__(self):
        self.publicaciones = []

    def agregar_publicacion(self, usuario_id, contenido):
        if not usuario_id or not contenido:
            raise ValueError("Todos los campos son obligatorios")
        if len(contenido) > 500:
            raise ValueError("La publicación no puede exceder los 500 caracteres")
        
        id = len(self.publicaciones) + 1
        fecha = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        publicacion = Publicacion(id, usuario_id, contenido, fecha)
        self.publicaciones.append(publicacion)
        print(f"Publicación agregada: {publicacion}")

    def listar_publicaciones(self):
        return self.publicaciones
    
    def eliminar_publicacion(self, id):
        self.publicaciones = [p for p in self.publicaciones if p.id != id]

    '''def actualizar_publicacion(self, id, contenido):
        for publicacion in self.publicaciones:
            if publicacion.id == id:
                publicacion.contenido = contenido
                break'''
    

    




    '''def delete_client(self, id):
        self.clientes = [client for client in self.clientes if client.id != id]

    def update_client(self, id, nombre, email):
        for cliente in self.clientes:
            if cliente.id == id:
                cliente.nombre = nombre
                cliente.email = email
                return True
        return False'''