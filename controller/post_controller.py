from models.client_model import *

class ClienteController:
    def __init__(self):
        self.clientes = []

    def get_client(self):
        return self.clientes

    def add_client(self, id, nombre, email):
        client = Client(id, nombre, email) # Estructura del modelo
        self.clientes.append(client)
    
    def delete_client(self, id):
        self.clientes = [client for client in self.clientes if client.id != id]

    def update_client(self, id, nombre, email):
        for cliente in self.clientes:
            if cliente.id == id:
                cliente.nombre = nombre
                cliente.email = email
                return True
        return False