from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse
from controller.user_controller import UsuarioController
from controller.post_controller import PublicacionController

controlador = UsuarioController()  # Creamos Objeto controlador de usuario
controlador_publicaciones = PublicacionController()  # Creamos Objeto controlador de publicaciones
sessions = {}  # Diccionario para almacenar las sesiones de los usuarios autenticados

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
        

        elif path == "/list":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            usuarios = controlador.get_user()
            lista_usuarios = "".join(
                f"<li>{usuario.id} {usuario.nombre} {usuario.email}</li>"
                for usuario in usuarios

            )
                # Renderizar el template con la lista de usuarios
            html_content = self.render_template('ListaUsuarios.html', {'usuarios': lista_usuarios})
            self.wfile.write(html_content.encode('utf-8'))
            return
        
        elif path == "/publicaciones":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            publicaciones = controlador_publicaciones.listar_publicaciones()
            lista_publicaciones = "".join(
                f"<li>{publicacion.id} {publicacion.usuario_id} {publicacion.contenido} {publicacion.fecha}</li>"
                for publicacion in publicaciones
            )

            # Renderizar el template con la lista de publicaciones
        
            html_content = self.render_template('Publicaciones.html', {'publicaciones': lista_publicaciones})
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
                    'usuario_email': usuario.email,
                    'usuario_password': usuario.password
                })
                self.wfile.write(html_content.encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"User not found")
        
        elif path == "/logout":
            session_id = self.headers.get('Cookie')
            if session_id in sessions:
                del sessions[session_id]
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing 'id' parameter")
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
            id = len(controlador.get_user()) + 1
            controlador.add_user(id, nombre, email, password)

            if not email:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("El correo electrónico no puede estar vacío".encode('utf-8'))
                return

            if len(password) < 8:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("La contraseña debe tener al menos 8 caracteres".encode('utf-8'))
                return
            

        elif path == "/update":
            id = int(parsed_data['id'][0])
            nombre = parsed_data['nombre'][0]
            email = parsed_data['email'][0]
            password = parsed_data['password'][0]
            controlador.update_user(id, nombre, email, password)

            if not email:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("El correo electrónico no puede estar vacío".encode('utf-8'))
                return

            if len(password) < 8:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("La contraseña debe tener al menos 8 caracteres".encode('utf-8'))
                return


        elif path == "/login":
            email = parsed_data['email'][0]
            password = parsed_data['password'][0]
            
            if not email:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("El correo electrónico no puede estar vacío".encode('utf-8'))
                return

            if len(password) < 8:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("La contraseña debe tener al menos 8 caracteres".encode('utf-8'))
                return

            if controlador.authenticate_user(email, password):
                session_id = str(len(sessions) + 1)
                sessions[session_id] = email
                self.send_response(303)
                self.send_header('Location', '/list')
                self.send_header('Set-Cookie', session_id)
                self.end_headers()
            else:
                self.send_response(401)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("Login failed".encode('utf-8'))
            return

        elif path == "/create_post":
            session_id = self.headers.get('Cookie')
            if session_id not in sessions:
                self.send_response(303)
                self.send_header('Location', '/login')
                self.end_headers()
                return

            email = sessions[session_id]
            usuario_autenticado = controlador.get_user_by_email(email)  # Método para obtener el usuario autenticado

            contenido = parsed_data['contenido'][0]
            usuario_id = usuario_autenticado.id
            

            try:
                controlador_publicaciones.agregar_publicacion(usuario_id, contenido)
                self.send_response(303)
                self.send_header('Location', '/publicaciones')
                self.end_headers()
            except ValueError as e:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
            return


        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

PORT = 8000

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

with HTTPServer(("", PORT), MyHandler) as httpd:
    print(f"Servidor ejecutado en el puerto {PORT}")
    httpd.serve_forever()