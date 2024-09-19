from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse
from controller.user_controller import UsuarioController

controlador = UsuarioController()  # Creamos Objeto controlador de usuario

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

            usuarios = controlador.get_user()
            lista_usuarios = "".join(
                f"<li>{usuario.id} {usuario.nombre} {usuario.email}"
                f"<a href='/delete?id={usuario.id}'> Eliminar </a> "
                f"<a href='/update?id={usuario.id}'> Actualizar </a> </li>"
                for usuario in usuarios
            )

            # Renderizar el template con la lista de usuarios
            html_content = self.render_template('index.html', {'usuarios': lista_usuarios})
            self.wfile.write(html_content.encode('utf-8'))
            return

        elif path == "/delete":
            query = urllib.parse.parse_qs(parsed_path.query)
            id = int(query['id'][0])
            controlador.delete_user(id)

            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()

        elif path == "/update":
            query = urllib.parse.parse_qs(parsed_path.query)
            id = int(query['id'][0])
            usuario = next((u for u in controlador.get_user() if u.id == id), None)

            if usuario:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Renderizar el template de actualización con los datos del usuario en update.html
                html_content = self.render_template('update.html', {
                    'usuario_id': str(usuario.id),
                    'usuario_name': usuario.nombre,
                    'usuario_email': usuario.email
                })
                self.wfile.write(html_content.encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
            return

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.parse_qs(post_data)

        if path == "/":
            nombre = parsed_data['nombre'][0]
            email = parsed_data['email'][0]
            password = parsed_data['password'][0]
            fecha_creacion = "2023-10-01"  # Puedes cambiar esto a la fecha actual
            id = len(controlador.get_user()) + 1
            controlador.add_user(id, nombre, email, password, fecha_creacion)

        elif path == "/update":
            id = int(parsed_data['id'][0])
            nombre = parsed_data['nombre'][0]
            email = parsed_data['email'][0]
            password = parsed_data['password'][0]
            fecha_creacion = parsed_data['fecha_creacion'][0]
            controlador.update_user(id, nombre, email, password, fecha_creacion)

        elif path == "/login":
            email = parsed_data['email'][0]
            password = parsed_data['password'][0]
            
            if controlador.authenticate_user(email, password):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Login successful")
            else:
                self.send_response(401)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Login failed")


        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

PORT = 8000

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

with HTTPServer(("", PORT), MyHandler) as httpd:
    print(f"Servidor ejecutado en el puerto {PORT}")
    httpd.serve_forever()