import serial
import tkinter as tk
import time
import threading



# VARIABLES GLOBALES #
ventana = None
canvas = None
vidas_label = None
puntos_label = None
estado_label = None

tamanio_ventana = (800, 600)
escala_ventana = (3, 3)

vidas = 3
puntos = 0

sprites = []



# FUNCIONES #
def iniciar_ventana():
    global ventana
    global canvas
    global vidas_label
    global puntos_label
    global estado_label
    
    ventana = tk.Tk()
    ventana.title("Juego del Topo")
    ventana.iconphoto(True, tk.PhotoImage(file="images/icon.png"))
    ventana.resizable(False, False)
    ventana.geometry(str(tamanio_ventana[0]) + "x" + str(tamanio_ventana[1]) + "+" + str((ventana.winfo_screenwidth() - tamanio_ventana[0]) // 2) + "+" + str((ventana.winfo_screenheight() - tamanio_ventana[1]) // 2))
    ventana.configure(bg="#89521b")
    
    canvas = tk.Canvas(ventana, width=tamanio_ventana[0], height=tamanio_ventana[1], bg="#89521b")
    
    estado_label = tk.Label(ventana, text="estado", font=("Arial", 16))
    vidas_label = tk.Label(ventana, text="vidas", font=("Arial", 16))
    puntos_label = tk.Label(ventana, text="puntos", font=("Arial", 16))

def actualizar_ventana():
    ventana.mainloop()

def leer_arduino():
    usb_arduino = serial.Serial("COM3", 9600)
    while True:
        linea = usb_arduino.readline().decode().strip()
        comando = linea.split(",")[0]
        argumentos = linea.split(",")
        argumentos.pop(0)
        if comando != "":
            ventana.after(0, globals()[str(comando) + "_func"], argumentos)
        time.sleep(1)

def results_menu():
    canvas.pack_forget()
    canvas.delete("all")

def game_menu():
    vidas_label.pack_forget()
    puntos_label.pack_forget()
    estado_label.pack_forget()
    sprites.clear()

def game_started_func(argumentos):
    game_menu()
    
    cantidad_de_columnas = int(argumentos[1])
    fila = 1
    columna = 0
    for i in range(0, int(argumentos[0]) * cantidad_de_columnas, 1):
        imagen = tk.PhotoImage(file="images/hole.png")
        if i == int(argumentos[2]) - 1:
            imagen = tk.PhotoImage(file="images/hole_with_mole.png")
        
        imagen = imagen.subsample(escala_ventana[0], escala_ventana[1])
        sprite = canvas.create_image((tamanio_ventana[0] / escala_ventana[0]) / 2, (tamanio_ventana[1] / escala_ventana[1]) / 2, image=imagen)
        sprites.append(imagen)
        sprites.append(sprite)
        if i % cantidad_de_columnas == 0 and i != 0:
            fila += 1
            columna = 1
        else:
            columna += 1
        canvas.coords(sprite, 160 * columna, (130 * fila) - 45)
    canvas.pack()

def game_results_func(argumentos):
    results_menu()
    
    vidas_label.config(text="Vidas: " + str(argumentos[0]))
    puntos_label.config(text="Puntos: " + str(argumentos[1]))
    estado_label.config(text="playing")

    estado_label.pack()
    vidas_label.pack()
    puntos_label.pack()
    
def game_over_func(argumentos):
    results_menu()
    
    vidas_label.config(text="Vidas: " + str(argumentos[0]))
    puntos_label.config(text="Puntos: " + str(argumentos[1]))
    estado_label.config(text="game over")

    estado_label.pack()
    vidas_label.pack()
    puntos_label.pack()



# MAIN #
iniciar_ventana()

hilo = threading.Thread(target=leer_arduino)
hilo.daemon = True
hilo.start()

actualizar_ventana()