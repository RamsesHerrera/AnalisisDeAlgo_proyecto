import socket
import os

def limpiar_pantalla():
    # Detectar el sistema operativo y ejecutar el comando correspondiente
    if os.name == 'nt':
        os.system('cls')  # Comando para Windows
    else:
        os.system('clear')  # Comando para Unix/Linux/Mac

def jugar(nombre_jugador):
    limpiar_pantalla()
    print(f"{nombre_jugador}, selecciona una opción:")
    print("1. Piedra")
    print("2. Papel")
    print("3. Tijeras")
    opcion = input("Ingresa el número correspondiente a tu elección: ")
    while opcion not in ['1', '2', '3']:
        print("Opción inválida. Por favor, selecciona 1, 2 o 3.")
        opcion = input("Ingresa el número correspondiente a tu elección: ")
    return opcion

def conectar_servidor():
    servidor_ip = "192.168.1.76"  # Dirección IP del servidor
    servidor_puerto = 9999

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((servidor_ip, servidor_puerto))

    # Obtener el nombre del jugador
    limpiar_pantalla()
    nombre_jugador = input("Ingresa tu nombre: ")

    # Enviar el nombre del jugador y su elección al servidor
    eleccion = jugar(nombre_jugador)
    mensaje = nombre_jugador + ',' + eleccion
    cliente_socket.send(mensaje.encode())

    # Limpiar la pantalla antes de mostrar los resultados
    limpiar_pantalla()

    # Recibir y mostrar el resultado del servidor
    print("Esperando resultados...")
    while True:
        resultado = cliente_socket.recv(1024).decode()
        if not resultado:
            break
        limpiar_pantalla()
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
    limpiar_pantalla()
