from http.server import HTTPServer, BaseHTTPRequestHandler
import requests 
import json


class clientes:
    def __init__(self, id, client, status, payment, order_type):
        self.id=id
        self.client=client
        self.status=status
        self.payment=payment
        self.order_type=order_type

#Consideranfo tipo de compra debemos ver si esta es digital o si es fisica
class Fisica(clientes):
    def __init__(self, shipping, products1, products2, products3):
        super().__init__(self, id=1, client="Juan Perez", status="Pendiente", payment="Tarjeta de Credito")
        self.shipping=shipping
        self.products1="Camiseta" 
        self.products2="Pantalon"
        self.products3="Zapatos"

class Digital(clientes):
    def __init__(self, code, expiration):
        super().__init__( self, id=2, client="Maria Rodriguez", status="Pendiente", payment="Paypal")
        self.code=code        
        self.expiration=expiration

class clientes_Factory:
    def create_cliente(self, order_type):
        if order_type == "Fisica":
            return Fisica()
        elif order_type == "Digital":
            return Digital()
        else:
            raise ValueError("Tipo de orden no válido")

    
class RESTRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
    
    def listar_id(self, id):
        return next(
            (cliente for cliente in clientes if cliente["id" == id]),
            None,
        )
    
    def pendientes(self, status):
        return next(
            (cliente for cliente in clientes if cliente["status"] == status),
            None,
        )
    
    def listar(self):
        return next(
            (cliente for cliente in clientes),
            None,
        )
    
    def eliminar_id(self, id):
        return next(
            (cliente for cliente in clientes if cliente["id" == id]),
            None,
        )    

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
    
    def do_GET(self):
        if self.path == "/clientes":
            self.send_response(200, clientes)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(clientes).encode("utf-8"))
        elif self.path.startswith("/clientes/"):
            cliente = self.listar_id(id)
            if cliente:
                self.response_handler(200, [cliente])
            else:
                self.response_handler(204, [])

            id = int(self.path.split("/")[-1])
            cliente = next(
                (cliente for cliente in clientes if cliente["id"] == id),
                None,
            )
            if cliente:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(cliente).encode("utf-8"))

        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"Error": "Ruta no existente"}).encode("utf-8"))

    def do_POST(self):
        if self.path == "/clientes":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data.decode("utf-8"))

            data = self.read_data()
            data["id"] = len(clientes) + 1
            clientes.append(data)
            self.response_handler(201, clientes)

            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(clientes).encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"Error": "Ruta no existente"}).encode("utf-8"))

    def do_PUT(self):
        if self.path.startswith("/clientes"):
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            status = data["status"]
            id = int(self.path.split("/")[-1])
            cliente = self.listar(status)
            data = self.read_data()
            cliente = next(
                (cliente for cliente in clientes if cliente["status"] == status),
                None,
            )
            if cliente:
                cliente.update(data)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(cliente).encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"Error": "Ruta no existente"}).encode("utf-8"))

    def do_DELETE(self):
        if self.path == "/clientes":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            clientes.clear()
            self.wfile.write(json.dumps(clientes).encode("utf-8"))
            cliente = self.eliminar_id(id)
            if cliente:
                self.response_handler(200, [cliente])
            else:
                self.response_handler(204, [])

            id = int(self.path.split("/")[-1])
            cliente = next(
                (cliente for cliente in clientes if cliente["id"] == id),
                None,
            )
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"Error": "Ruta no existente"}).encode("utf-8"))
    

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()
