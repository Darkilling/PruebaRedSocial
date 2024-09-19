from models.usuario_model import *

class UserControlador:
    
        def __init__(self):
            self.usuarios = []
            

        def get_user(self):
            return self.usuarios
        
        def add_user(self, id, nombre, email, password, fecha_creacion):
            for usuarios in self.usuarios:
                if usuarios.nombre == nombre:
                    print(f"Este cliente ya está en la lista", usuarios.id, usuarios.nombre, usuarios.email, usuarios.password, usuarios.fecha_creacion)
                    return False
            
            usuarios = user(id, nombre, email, password, fecha_creacion)
            self.usuarios.append(user)
            return True
        
        def delete_client(self, id):
         self.usuarios = [user for user in self.usuarios if user.id != id]
    
        def update_user(self, id, nombre, email, password, fecha_creacion):
            for usuarios in self.usuarios:
                if usuarios.id == id:
                    usuarios.id = id
                    usuarios.nombre = nombre
                    usuarios.email = email
                    usuarios.password = password
                    usuarios.fecha_creacion = fecha_creacion
                return True
            return False
