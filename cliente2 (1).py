import socket

def jugar():
    print("Selecciona una opción:")
    print("1. Piedra")
    print("2. Papel")
    print("3. Tijeras")
    opcion = input("Ingresa el número correspondiente a tu elección: ")
    while opcion not in ['1', '2', '3']:
        print("Opción inválida. Por favor, selecciona 1, 2 o 3.")
        opcion = input("Ingresa el número correspondiente a tu elección: ")
    if opcion == '1':
        return "piedra"
    elif opcion == '2':
        return "papel"
    else:
        return "tijeras"


def conectar_servidor():
    servidor_ip = "148.210.89.229"  # Dirección IP del servidor anterior
    servidor_puerto = 9999

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((servidor_ip, servidor_puerto))

    # Obtener el nombre del jugador
    nombre_jugador = input("Ingresa tu nombre: ")

    # Enviar el nombre del jugador y su elección al servidor
    eleccion = jugar()
    mensaje = nombre_jugador + ',' + eleccion
    cliente_socket.send(mensaje.encode())

    # Recibir y mostrar el resultado del servidor
    while True:
        resultado = cliente_socket.recv(1024).decode()
        if not resultado:
            break
        print(resultado)

    # Cerrar la conexión
    cliente_socket.close()

def jugar_nueva_partida():
    respuesta = input("¿Deseas jugar una nueva partida? (s/n): ")
    return respuesta.lower() == "s"

while True:
    conectar_servidor()
    if not jugar_nueva_partida():
        break
