import socket
import tkinter as tk
from tkinter import messagebox

def limpiar_pantalla():
    for widget in root.winfo_children():
        widget.destroy()

def jugar(nombre_jugador):
    limpiar_pantalla()
    tk.Label(root, text=f"{nombre_jugador}, selecciona una opción:").pack(pady=10)
    opciones = ["Piedra", "Papel", "Tijeras"]
    var_opcion = tk.StringVar(value=opciones[0])
    
    for opcion in opciones:
        tk.Radiobutton(root, text=opcion, variable=var_opcion, value=opcion).pack(anchor=tk.W)
    
    tk.Button(root, text="Enviar", command=lambda: enviar_eleccion(nombre_jugador, var_opcion.get())).pack(pady=10)

def conectar_servidor(nombre_jugador, eleccion):
    servidor_ip = "148.210.173.202"  # Dirección IP del servidor
    servidor_puerto = 9999

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((servidor_ip, servidor_puerto))

    # Enviar el nombre del jugador y su elección al servidor
    eleccion_num = {"Piedra": "1", "Papel": "2", "Tijeras": "3"}[eleccion]
    mensaje = nombre_jugador + ',' + eleccion_num
    cliente_socket.send(mensaje.encode())

    # Limpiar la pantalla y mostrar mensaje de espera
    limpiar_pantalla()
    tk.Label(root, text="Esperando resultados...").pack(pady=20)

    # Recibir y mostrar el resultado del servidor
    resultados = ""
    while True:
        resultado = cliente_socket.recv(1024).decode()
        if not resultado:
            break
        resultados += resultado + "\n"

    limpiar_pantalla()
    tk.Label(root, text="Resultados:").pack(pady=10)
    tk.Label(root, text=resultados).pack(pady=10)

    tk.Button(root, text="Jugar otra vez", command=iniciar).pack(pady=5)
    tk.Button(root, text="Salir", command=root.quit).pack(pady=5)

    # Cerrar la conexión
    cliente_socket.close()

def enviar_eleccion(nombre_jugador, eleccion):
    conectar_servidor(nombre_jugador, eleccion)

def iniciar():
    limpiar_pantalla()
    tk.Label(root, text="Ingresa tu nombre:").pack(pady=10)
    nombre_entry = tk.Entry(root)
    nombre_entry.pack(pady=10)
    tk.Button(root, text="Ingresar", command=lambda: jugar(nombre_entry.get())).pack(pady=10)

root = tk.Tk()
root.title("Piedra, Papel o Tijeras")
root.geometry("400x300")

iniciar()

root.mainloop()
