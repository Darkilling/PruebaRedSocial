from models.usuario_model import Usuario

class UsuarioController:
    def __init__(self):
        self.usuarios = []

    def get_user(self):
        return self.usuarios

    def add_user(self, id, nombre, email, password, fecha_creacion):
        usuario = Usuario(id, nombre, email, password, fecha_creacion)
        self.usuarios.append(usuario)
    
    def delete_user(self, id):
        self.usuarios = [usuario for usuario in self.usuarios if usuario.id != id]

    def update_user(self, id, nombre, email, password, fecha_creacion):
        for usuario in self.usuarios:
            if usuario.id == id:
                usuario.nombre = nombre
                usuario.email = email
                usuario.password = password
                usuario.fecha_creacion = fecha_creacion
                return True
        return False