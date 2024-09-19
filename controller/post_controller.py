from models.client_model import *

class ClienteController:
    def __init__(self):
        self.clientes = []

    def get_client(self):
        return self.clientes

    def add_client(self, id, nombre, email, telefono, direccion, apellido, rut):
        for cliente in self.clientes:
            if cliente.rut == rut:
                print(f"Este cliente ya está en la lista", cliente.rut, cliente.nombre, cliente.apellido)
                return False
        
        client = Client(id, nombre, email, telefono, direccion, apellido, rut)
        self.clientes.append(client)
        return True
    
    def delete_client(self, id):
        self.clientes = [client for client in self.clientes if client.id != id]
    
    def update_client(self, id, nombre, email, telefono, direccion, apellido, rut):
        for cliente in self.clientes:
            if cliente.id == id:
                cliente.rut = rut
                cliente.nombre = nombre
                cliente.apellido = apellido                
                cliente.email = email
                cliente.telefono = telefono
                cliente.direccion = direccion
                return True
        return False
