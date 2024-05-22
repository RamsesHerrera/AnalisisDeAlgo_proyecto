import socket
import time
num_jugadores = 4
def jugar_ppt(jugadores):
    resultados = {}
    puntos = {}
    for jugador in jugadores:
        puntos[jugador] = 0

    for jugador, eleccion in jugadores.items():
        resultados[jugador] = []
        for adversario, adversario_eleccion in jugadores.items():
            if jugador != adversario:
                if eleccion == adversario_eleccion:
                    resultados[jugador].append(f"{jugador} empate con {adversario}")
                elif (eleccion == "1" and adversario_eleccion == "3") or \
                     (eleccion == "2" and adversario_eleccion == "1") or \
                     (eleccion == "3" and adversario_eleccion == "2"):
                    resultados[jugador].append(f"{jugador} gana contra {adversario}")
                else:
                    resultados[jugador].append(f"{jugador} pierde contra {adversario}")
    
    # Calcular puntos después de determinar resultados
    for jugador, result_list in resultados.items():
        for result in result_list:
            if "gana contra" in result:
                puntos[jugador] += 3
            elif "empate con" in result:
                puntos[jugador] += 1
            elif "pierde contra" in result:
                puntos[jugador] -= 1

    return resultados, puntos

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
        if len(jugadores) == num_jugadores: # Cambiado para admitir 4 jugadores
            # Calcular los resultados y los puntos
            resultados, puntos = jugar_ppt(jugadores)

            # Enviar los resultados a los jugadores
            for jugador, result_list in resultados.items():
                socket_cliente = sockets_clientes[jugador]
                socket_cliente.send(f"Tus resultados:\n".encode())
                for result in result_list:
                    socket_cliente.send(result.encode())
                    socket_cliente.send("\n".encode())

            # Determinar el ganador
            ganador = max(puntos, key=puntos.get)
            puntaje_ganador = puntos[ganador]
            mensaje_ganador = f"El ganador es {ganador} con {puntaje_ganador} puntos.\n"

            # Ordenar los jugadores por puntos de mayor a menor
            puntos_ordenados = sorted(puntos.items(), key=lambda x: x[1], reverse=True)

            # Enviar las puntuaciones ordenadas y el ganador a los jugadores
            for jugador, socket_cliente in sockets_clientes.items():
                socket_cliente.send("\nPuntuaciones finales:\n".encode())
                for jugador_puntos, puntaje in puntos_ordenados:
                    socket_cliente.send(f"{jugador_puntos}: {puntaje} puntos\n".encode())
                socket_cliente.send(mensaje_ganador.encode())

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
    servidor_ip = "192.168.1.76"  # Dirección IP del servidor
    servidor_puerto = 9999 # Cambiado el puerto para manejar más tráfico

    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((servidor_ip, servidor_puerto))
    servidor_socket.listen(num_jugadores) # Aumentado el número máximo de conexiones en espera a 4

    print("Servidor escuchando en", servidor_ip, "puerto", servidor_puerto)

    jugadores = {}
    sockets_clientes = {}
    
    while True:
        print("Esperando jugadores...")
        
        while len(jugadores) < num_jugadores: # Cambiado para admitir 4 jugadores
            cliente_socket, cliente_direccion = servidor_socket.accept()
            manejar_conexion(cliente_socket, cliente_direccion, jugadores, sockets_clientes)

iniciar_servidor()
