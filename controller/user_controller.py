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
        user = next((u for u in self.usuarios if u.email == email and u.password == password), None)
        return user is not None

    def get_user_by_email(self, email):
        return next((u for u in self.usuarios if u.email == email), None)