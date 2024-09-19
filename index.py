from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse
from controller.user_controller import UserControlador

UserControlador = UserControlador() #Creamos Obejto controlador de cliente

class MyHandler(BaseHTTPRequestHandler):
    def render_template(self, template_name, context):
        try:
            with open(f'view/{template_name}', 'r', encoding='utf-8') as file:
                template = file.read()
            # Aquí puedes agregar lógica para reemplazar variables en el template con valores del contexto
            return template
        except FileNotFoundError:
            self.send_error(404, f"File {template_name} not found")
            return None

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
            user = next((u for u in UserControlador.get_user() if u.id == id ), None)
            #id,nombre,email,telefono,direccion,apellido,rut
            if user:
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                html_content = self.render_template('update.html', {
                    'user_id': str(user.id),
                    'user_name': user.nombre,
                    'user_email': user.email,
                    'user_password': user.password,
                    'user_fecha_creacion': user.fecha_creacion
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
            id = len(UserControlador.get_user())
            nombre = parsed_data['nombre'][0]
            email = parsed_data['email'][0]

            UserControlador.add_user(id +1, nombre, email, password, fecha_creacion)
            print(UserControlador.get_user())

        elif path == "/update":
            id = int(parsed_data['id'][0])
            nombre = parsed_data['nombre'][0]
            email = parsed_data['email'][0]
            password = parsed_data['password'][0]
            fecha_creacion = parsed_data['fecha_creacion'][0]

            UserControlador.update_user(id, nombre, email, password, fecha_creacion)

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

PORT = 8000

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

with HTTPServer(("", PORT), MyHandler) as httpd:
    print(f"Servidor ejecutado en el puerto {PORT}")
    httpd.serve_forever()