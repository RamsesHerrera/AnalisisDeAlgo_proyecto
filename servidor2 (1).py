import socket
import time

def jugar_ppt(jugadores):
    resultados = {}
    for jugador, eleccion in jugadores.items():
        resultados[jugador] = []
        for adversario, adversario_eleccion in jugadores.items():
            if jugador != adversario:
                if eleccion == adversario_eleccion:
                    resultados[jugador].append(f"{jugador} empate con {adversario}")
                elif (eleccion == 1 and adversario_eleccion == 3) or \
                     (eleccion == 2 and adversario_eleccion == 1) or \
                     (eleccion == 3 and adversario_eleccion == 2):
                    resultados[jugador].append(f"{jugador} gana contra {adversario}")
                else:
                    resultados[jugador].append(f"{jugador} pierde contra {adversario}")
    return resultados


def manejar_conexion(cliente_socket, cliente_direccion, jugadores, sockets_clientes):
    print("Conexión establecida desde:", cliente_direccion)

    try:
        # Recibir el nombre del jugador y su elección
        mensaje = cliente_socket.recv(1024).decode()
        nombre, eleccion = mensaje.split(',')
        print("Jugador", nombre, "eligio:", eleccion)

        # Agregar el nombre y la elección al diccionario de jugadores
        jugadores[nombre] = eleccion
        # Agregar el socket del cliente a la lista de sockets
        sockets_clientes[nombre] = cliente_socket

        # Verificar si todos los jugadores han elegido
        if len(jugadores) == 4: # Cambiado para admitir 4 jugadores
            # Calcular los resultados
            resultados = jugar_ppt(jugadores)

            # Enviar los resultados a los jugadores
            for jugador, result_list in resultados.items():
                socket_cliente = sockets_clientes[jugador]
                socket_cliente.send(f"Tus resultados:\n".encode())
                for result in result_list:
                    socket_cliente.send(result.encode())
                    socket_cliente.send("\n".encode())

            # Vaciar el diccionario de jugadores y la lista de sockets para una nueva partida
            jugadores.clear()
            sockets_clientes.clear()

            # Esperar un poco antes de cerrar la conexión para que los jugadores puedan ver el resultado
            time.sleep(1)
            cliente_socket.close()

    except Exception as e:
        print("Error en la conexión:", e)

    print("Conexión cerrada con:", cliente_direccion)

def iniciar_servidor():
    servidor_ip = "148.210.89.229"  # Dirección IP del servidor
    servidor_puerto = 9999 # Cambiado el puerto para manejar más tráfico

    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((servidor_ip, servidor_puerto))
    servidor_socket.listen(4) # Aumentado el número máximo de conexiones en espera a 4

    print("Servidor escuchando en", servidor_ip, "puerto", servidor_puerto)

    jugadores = {}
    sockets_clientes = {}
    
    while True:
        print("Esperando jugadores...")
        
        while len(jugadores) < 4: # Cambiado para admitir 4 jugadores
            cliente_socket, cliente_direccion = servidor_socket.accept()
            manejar_conexion(cliente_socket, cliente_direccion, jugadores, sockets_clientes)

iniciar_servidor()
