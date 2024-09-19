from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse
from controller.user_controller import UserControlador

UserControlador = UserControlador() #Creamos Obejto controlador de cliente

class MyHandler(BaseHTTPRequestHandler):

    def render_template(self, template_name, context):
        with open(f'view/{template_name}', 'r', encoding='utf-8') as file:
            html_content = file.read()
            for key, value in context.items():
                html_content = html_content.replace(f"{{{{{key}}}}}", value)
            return html_content

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Generar la lista de clientes
            usuarios = UserControlador.get_user()
            #id,nombre,email,telefono,direccion,apellido,rut
            lista_usuarios = "".join(
                f"<tr>"
                f"<td>{usuario.id}</td>"
                f"<td>{usuario.nombre}</td>"
                f"<td>{usuario.email}</td>"
                f"<td>"
                f"<a href='/delete?id={usuario.id}'>Eliminar</a> | "
                f"<a href='/update?id={usuario.id}'>Actualizar</a>"
                f"</td>"
                f"</tr>"
                for usuario in usuarios
            )
            

            #Renderizamos el template con la lista de clientes
            html_content = self.render_template('index.html', {'usuarios': lista_usuarios} )
            self.wfile.write(html_content.encode())
            return
        
        elif path == "/update":
            query = urllib.parse.parse_qs(parsed_path.query)
            id = int(query['id'][0])
            user = next((u for u in UserControlador.get_client() if u.id == id ), None)
            #id,nombre,email,telefono,direccion,apellido,rut
            if client:
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                html_content = self.render_template('update.html', {
                    'user_id': str(user.id),
                    'user_name': user.nombre,
                    'user_email': user.email,
                    'user_apell': user.password,
                    'user_fecha': user.fecha_creacion
                })

                self.wfile.write(html_content.encode())
            else:
                self.send_response(404)
                self.end_headers()
            return
        
        elif path == "/delete":
            query = urllib.parse.parse_qs(parsed_path.query)
            id = int(query['id'][0])
            UserControlador.delete_user(id)

            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            return
        
    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.parse_qs(post_data)

        #id,nombre,email,telefono,direccion,apellido,rut

        if path == "/":
            id = len(clienteControlador.get_client())
            nombre = parsed_data['nombre'][0]
            email = parsed_data['email'][0]
            telefono = parsed_data['telefono'][0]
            direccion = parsed_data['direccion'][0]
            apellido = parsed_data['apellido'][0]
            rut = parsed_data['rut'][0]

            clienteControlador.add_client(id +1, nombre, email, telefono, direccion, apellido, rut)
            print(clienteControlador.get_client())

        elif path == "/update":
            id = int(parsed_data['id'][0])
            nombre = parsed_data['nombre'][0]
            email = parsed_data['email'][0]
            telefono = parsed_data['telefono'][0]
            direccion = parsed_data['direccion'][0]
            apellido = parsed_data['apellido'][0]
            rut = parsed_data['rut'][0]

            clienteControlador.update_client(id, nombre, email,telefono, direccion, apellido, rut)

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

PORT = 8000

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

with HTTPServer(("", PORT), MyHandler) as httpd:
    print(f"Servidor ejecutado en el puerto {PORT}")
    httpd.serve_forever()