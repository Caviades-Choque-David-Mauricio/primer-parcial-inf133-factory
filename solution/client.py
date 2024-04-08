import requests

url = "http://localhost:8000/"

ruta_post = url + "clientes"
ruta_get = url + "clientes"
headers = {"Content-Type": "application/json"}


orden_type = "Fisico"
data = {"orden_type": orden_type}

# Hacemos una petición POST a la URL con los datos y encabezados definidos
response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print(response.text)
else:
    print("Error:", response.text)

orden_type = "Digital"
data = {"orden_type": orden_type}

# Hacemos otra petición POST a la URL con los nuevos datos y los mismos encabezados
response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print(response.text)
else:
    print("Error:", response.text)

get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)


# DELETE 
ruta_eliminar = url + "clientes"
eliminar_response = requests.request(method="DELETE", 
                                    url=ruta_eliminar)
print(eliminar_response.text)

# POST agrega 
ruta_post = url + "clientes"
nuevo_cliente = {

}

post_response = requests.request(method="POST", 
                        url=ruta_post,
                        json=nuevo_cliente)
print(post_response.text)

post_response = requests.request(method="POST", url=ruta_post, json=nuevo_cliente)
print(post_response.text)

# GET busca 
ruta_filtrar_nombre = url + "clientes/1"
filtrar_nombre_response = requests.request(method="GET", 
                                url=ruta_filtrar_nombre)
print(filtrar_nombre_response.text)

# PUT actualiza un estudiante por la ruta /estudiantes
ruta_actualizar = url + "clientes"
cliente_actualizado = {
    "id": 3,
    "client": "Ana Gutierrez",
    "status": "Pendiente",
    "payment": "Tarjeta de Debito",
}

orden_type = "Fisico"
data = {"orden_type": orden_type}

fisico_actualizado={
    "shippping": "20",
    "products1": "Licuadora",
    "products2": "Lavadora",
    "products3": "Refrigeradora",
}

digital_actualizado={
    "code":"XYE456",
    "expire":"2023-12-12",
}
put_response = requests.request(
    method="PUT", url=ruta_actualizar, 
    json=cliente_actualizado
)
put_response = requests.request(
    method="PUT", url=ruta_actualizar, 
    json=fisico_actualizado
)

put_response = requests.request(
    method="PUT", url=ruta_actualizar, 
    json=digital_actualizado
)
print(put_response.text)
