from tkinter import *
from tkinter import ttk
from SimonVirtual3D import SimonVirtual3D
from ObjectEncoder import ObjectEncoder
from GestorJugadores import GestorJugadores

class InterfazInicial():
    __ventana_inicial = None

    def salirPrograma(self):
        self.__ventana_inicial.destroy()

    def __init__(self):
        self.__ventana_inicial = Tk()
        self.__ventana_inicial.title("Nuevo Jugador ")
        self.__ventana_inicial.geometry("290x300")
        self.__ventana_inicial.resizable(0, 0)
        self.puntaje = IntVar()
        self.puntaje.set(0)
        self.nombre_jugador = StringVar()
        self.nombre_jugador.set("")
        self.ventana_interfaz = LabelFrame(self.__ventana_inicial, text = "Datos del Jugador", background = "black", foreground="white", highlightbackground = "black", relief = "raised", borderwidth = 1)
        self.ventana_interfaz.pack(fill = "both", expand = True)
        self.imagen = PhotoImage(file = "2c177ab7e028e004d8e697a97b7db5d4.png")
        bg_label = Label(self.ventana_interfaz, image = self.imagen).place(x = 0, y = 0, width = 290, height=290)
        self.iniciar_juego = ttk.Button(self.ventana_interfaz, text = "Iniciar", command = self.iniciarJuego)
        self.iniciar_juego.place(x = 110, y = 135)
        Label(self.ventana_interfaz, text = "Jugador" , bg="black", fg = "white").place(x = 45, y = 5)
        ttk.Entry(self.ventana_interfaz, textvariable = self.nombre_jugador).place(x = 120, y = 5)
        self.__ventana_inicial.mainloop()

    def iniciarJuego(self):
        jsonF = ObjectEncoder()
        gestor_jugadores = GestorJugadores()
        diccionario_partidas = jsonF.leerJSONArchivo("pysimonpuntajes.json")
        if diccionario_partidas != 0:
            print("EL ARCHIVO TIENE DATOS GUARDADOS")
            gestor_jugadores = jsonF.decodificadorDiccionario(diccionario_partidas)
        else:
            print("EL ARCHIVO NO TIENE DATOS GUARDADOS")
            diccionario_partidas = gestor_jugadores.toJSON()
            jsonF.guardarJSONArchivo(diccionario_partidas, "pysimonpuntajes.json")
        gestor_jugadores.addJugador(self.nombre_jugador.get(), self.puntaje.get())
        SimonVirtual3D(gestor_jugadores)
