from models.usuario_model import Usuario

class UsuarioController:
    def __init__(self):
        self.usuarios = []

    def get_user(self):
        return self.usuarios

    def add_user(self, id, nombre, email, password):
        usuario = Usuario(id, nombre, email, password)
        self.usuarios.append(usuario)
    
    def delete_user(self, id):
        self.usuarios = [usuario for usuario in self.usuarios if usuario.id != id]

    def update_user(self, id, nombre, email, password):
        for usuario in self.usuarios:
            if usuario.id == id:
                usuario.nombre = nombre
                usuario.email = email
                usuario.password = password
                return True
        return False
    
    def authenticate_user(self, email, password):
        for usuario in self.usuarios:
            if usuario.email == email and usuario.password == password:
                return True
        return False
