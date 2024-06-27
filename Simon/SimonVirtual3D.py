from tkinter import *
from ObjectEncoder import ObjectEncoder
import time
import random
from os import system
from tkinter import ttk

class SimonVirtual3D:
    __ventana: object
    __boton_verde: object
    __boton_rojo: object
    __boton_amarillo: object
    __boton_azul: object
    __lista_colores_maquina: list
    __lista_colores_usuario: list
    __tiempo: float

    def mostrarPuntaje(self):
        self.__ventana_puntajes = Toplevel()
        self.__ventana_puntajes.geometry("822x270")
        self.__panel_puntajes = ttk.Labelframe(self.__ventana_puntajes, text = "Galeria de Puntajes")
        self.__panel_puntajes.pack(fill = "both", expand = True)
        self.__panel_lista_puntajes = Frame(self.__panel_puntajes)
        self.__panel_lista_puntajes.grid(row = 1, column = 0)
        self.__panel_lista_puntajes.grid(sticky = "nswe", columnspan=4, rowspan = 4)
        self.__encabezados = ['Jugador', 'Fecha', 'Hora', 'Puntaje']
        self.lista_puntajes = ttk.Treeview(self.__panel_lista_puntajes, columns = self.__encabezados, show = 'headings')
        barra_desplazamiento = Scrollbar(self.__panel_lista_puntajes, command = self.lista_puntajes.yview)
        self.lista_puntajes.config(yscrollcommand = barra_desplazamiento.set)
        barra_desplazamiento.pack(side = RIGHT, fill = Y)
        self.lista_puntajes.pack(side = LEFT, fill = BOTH, expand = 1)
        ttk.Button(self.__ventana_puntajes, text = "cerrar", command = self.__ventana_puntajes.destroy).pack()
        for encabezado in self.__encabezados:
            self.lista_puntajes.heading(encabezado, text = encabezado)
            self.lista_puntajes.column(encabezado, anchor = "center")
        self.diccionario_partidas = self.jsonF.leerJSONArchivo("pysimonpuntajes.json")
        self.gestor_jugadores = self.jsonF.decodificadorDiccionario(self.diccionario_partidas)
        self.gestor_jugadores.ordenar_por_puntaje()
        lista_jugadores = self.gestor_jugadores.getListaJugadores()
        for jugador in lista_jugadores:
            nombre = jugador.getNombreJugador()
            fecha = jugador.getFechaPartida()
            hora = jugador.getHoraPartida()
            puntaje = jugador.getPuntajeJugador()
            jugador_data  = [nombre, fecha, hora, puntaje]
            self.lista_puntajes.insert('', 'end', values = jugador_data)
        self.__ventana_puntajes.wait_window()
    
    def ventanaGameOver(self):
        self.ventana_game_over = Toplevel()
        self.ventana_game_over.geometry("200x200")
        self.ventana_game_over.title("GAME OVER")
        Label(self.ventana_game_over, text = "GAME OVER").pack()
        Label(self.ventana_game_over, text = f"Puntuación Final: {self.puntuacion}").pack()
        self.guardarPartida()
        self.ventana_game_over.wait_window()

    def guardarPartida(self):
        self.jugador.setPuntajeJugador(self.puntuacion)
        self.gestor_jugadores.guardarPartida(self.jugador)
        self.diccionario_partidas = self.gestor_jugadores.toJSON()
        self.jsonF.guardarJSONArchivo(self.diccionario_partidas, "pysimonpuntajes.json")

    def salirPrograma(self):
        self.__ventana.destroy()
    
    def iluminarBoton(self):
        self.boton_seleccionado.config(bg = self.colores_iluminados[self.posicion_color_iluminado])
    
    def apagarBoton(self):
        time.sleep(0.15)
        self.boton_seleccionado.config(bg = self.color_original) 

    def apretarBoton(self, evento):
        self.boton_seleccionado.config(bg = self.colores_iluminados[self.posicion_color_iluminado], relief = "sunken")
        self.boton_seleccionado.bind('<ButtonRelease-1>', self.soltarBoton)

    def soltarBoton(self, evento):
        time.sleep(0.1)
        self.boton_seleccionado.config(bg = self.color_original, relief = "raised")

    def elegirBotonIluminar(self, boton, posicion_iluminado):
        self.boton_seleccionado = boton
        self.color_original = self.colores_originales[posicion_iluminado]
        self.posicion_color_iluminado = posicion_iluminado
        self.iluminarBoton()
        time.sleep(self.__tiempo)
        self.__ventana.update()
        self.apagarBoton()
        time.sleep(self.__tiempo)
        self.__ventana.update()

    def iluminarColor(self, posicion_color):
        self.__ventana.update()
        if self.__lista_colores_maquina[posicion_color] == "green":
            self.elegirBotonIluminar(self.__boton_verde, 0)
        elif self.__lista_colores_maquina[posicion_color] == "red":
            self.elegirBotonIluminar(self.__boton_rojo, 1)
        elif self.__lista_colores_maquina[posicion_color] == "yellow":
            self.elegirBotonIluminar(self.__boton_amarillo, 2)
        elif self.__lista_colores_maquina[posicion_color] == "blue":
            self.elegirBotonIluminar(self.__boton_azul, 3)

    def elegirBotonMemorizar(self):
        self.__boton_verde.bind('<ButtonPress-1>', lambda event: self.compararSencuencia(self.__boton_verde))
        self.__boton_rojo.bind('<ButtonPress-1>', lambda event: self.compararSencuencia(self.__boton_rojo))
        self.__boton_amarillo.bind('<ButtonPress-1>', lambda event: self.compararSencuencia(self.__boton_amarillo))
        self.__boton_azul.bind('<ButtonPress-1>', lambda event: self.compararSencuencia(self.__boton_azul))

    def comenzarSecuencia(self):
        self.__ventana.update()
        time.sleep(0.6)
        color_generado = str(random.choice(self.__lista_colores))
        self.__lista_colores_maquina.append(color_generado)
        for posicion_color in range(len(self.__lista_colores_maquina)):
            print(f"Color nro: {posicion_color + 1}: {self.__lista_colores_maquina[posicion_color]}")
            self.iluminarColor(posicion_color)
        self.elegirBotonMemorizar()

    def agregarColorUsuario(self):
        if self.color_original == self.colores_originales[0]:
            self.__lista_colores_usuario.append("green")
            self.posicion_color_iluminado = 0
        elif self.color_original == self.colores_originales[1]:
            self.__lista_colores_usuario.append("red")
            self.posicion_color_iluminado = 1
        elif self.color_original == self.colores_originales[2]:
            self.__lista_colores_usuario.append("yellow")
            self.posicion_color_iluminado = 2
        elif self.color_original == self.colores_originales[3]:
            self.__lista_colores_usuario.append("blue")
            self.posicion_color_iluminado = 3

    def cerearPartida(self):
        self.__lista_colores_maquina.clear()
        self.__lista_colores_usuario.clear()
        self.posicion_color_comparador = 0
        self.puntuacion = 0
        self.marcador_puntos.config(text = self.puntuacion)
        self.__boton_rojo["bg"] = self.colores_originales[1]
        self.__boton_azul["bg"] = self.colores_originales[3]
        self.__boton_amarillo["bg"] = self.colores_originales[2]
        self.__boton_verde["bg"] = self.colores_originales[0]

    def aumentarDificultad(self):
        self.puntuacion += 1
        self.marcador_puntos.config(text = self.puntuacion)
        if self.__tiempo >= 0.1:
            self.__tiempo -= 0.15
        else:
            self.__tiempo = 0.04
    
    def empezarOtraVez(self):
        self.empezar = False
        match self.opcion.current():
            case 0: self.__tiempo = 3
            case 1: self.__tiempo = 2
            case 2: self.__tiempo = 0.85
        self.cerearPartida()
        self.iniciarSecuenciaInicioUno()
        self.presionarBotonIniciar()

    def despegarBotones(self):
        self.__boton_verde.config(relief = "raised")
        self.__boton_rojo.config(relief = "raised")
        self.__boton_amarillo.config(relief = "raised")
        self.__boton_azul.config(relief = "raised")

    def compararSencuencia(self, boton):
        system("cls")
        self.posicion_color_iluminado = 0
        self.boton_seleccionado = boton
        self.color_original = str(self.boton_seleccionado["bg"])
        self.agregarColorUsuario()
        print(f"Color agregado a usuario: {self.__lista_colores_usuario} - {len(self.__lista_colores_usuario)} colores en total")
        print(f"Colores de la maquina: {self.__lista_colores_maquina} - {len(self.__lista_colores_maquina)} colores en total")
        if self.__lista_colores_maquina[self.posicion_color_comparador] != self.__lista_colores_usuario[self.posicion_color_comparador]:
            print(f"\n{self.__lista_colores_maquina[self.posicion_color_comparador]} y {self.__lista_colores_usuario[self.posicion_color_comparador]} NO son iguales")
            print("\nPERDISTE")
            self.despegarBotones()
            self.iniciarSecuenciaInicioDos()
            self.ventanaGameOver()
            self.empezarOtraVez()
        else:
            self.apretarBoton(evento=None)
            self.posicion_color_comparador += 1
        if self.posicion_color_comparador == len(self.__lista_colores_maquina):
            print("\nNivel Superado:\n")
            self.__lista_colores_usuario.clear()
            self.posicion_color_comparador = 0
            self.aumentarDificultad()
            self.comenzarSecuencia()

    def iniciarSecuenciaInicioUno(self):
        time.sleep(0.11)
        self.__boton_rojo["bg"] = self.colores_iluminados[1]
        self.__ventana.update()
        time.sleep(0.11)
        self.__boton_rojo["bg"] = self.colores_originales[1]
        self.__ventana.update()
        time.sleep(0.11)
        self.__boton_azul["bg"] = self.colores_iluminados[3]
        self.__ventana.update()
        time.sleep(0.11)
        self.__boton_azul["bg"] = self.colores_originales[3]
        self.__ventana.update()
        time.sleep(0.11)
        self.__boton_amarillo["bg"] = self.colores_iluminados[2]
        self.__ventana.update()
        time.sleep(0.11)
        self.__boton_amarillo["bg"] = self.colores_originales[2]
        self.__ventana.update()
        time.sleep(0.11)
        self.__boton_verde["bg"] = self.colores_iluminados[0]
        self.__ventana.update()
        time.sleep(0.11)
        self.__boton_verde["bg"] = self.colores_originales[0]
        self.__ventana.update()
        time.sleep(0.11)
        self.__ventana.update()
    
    def iniciarSecuenciaInicioDos(self):
        for posicion_secuencia in range(3):
            time.sleep(0.13)
            self.__boton_rojo["bg"] = self.colores_iluminados[1]
            self.__boton_azul["bg"] = self.colores_iluminados[3]
            self.__boton_amarillo["bg"] = self.colores_iluminados[2]
            self.__boton_verde["bg"] = self.colores_iluminados[0]
            self.__ventana.update()
            time.sleep(0.13)
            self.__boton_rojo["bg"] = self.colores_originales[1]
            self.__boton_azul["bg"] = self.colores_originales[3]
            self.__boton_amarillo["bg"] = self.colores_originales[2]
            self.__boton_verde["bg"] = self.colores_originales[0]
            self.__ventana.update()

    def dale(self):
        self.empezar = True
    
    def presionarBotonIniciar(self):
        self.__boton_verde.bind('<ButtonPress-1>', lambda event: self.dale())
        for repeticion_color_verde in range(999):
            if self.empezar != True:
                time.sleep(0.8)
                self.__boton_verde["bg"] = self.colores_iluminados[0]
                self.__ventana.update()
                time.sleep(0.8)
                self.__boton_verde["bg"] = self.colores_originales[0]
                self.__ventana.update()
            else:
                return self.comenzarSecuencia()

    def empezarNivel(self):
        self.empezar = False
        match self.opcion.current():
            case 0: self.__tiempo = 3
            case 1: self.__tiempo = 2
            case 2: self.__tiempo = 0.85
        self.posicion_color_comparador = 0
        self.__lista_colores_usuario = []
        self.__lista_colores_maquina = []
        self.cerearPartida()
        self.iniciarSecuenciaInicioUno()
        self.iniciarSecuenciaInicioUno()
        self.iniciarSecuenciaInicioDos()
        self.presionarBotonIniciar()


    def __init__(self, gestor_jugadores):
        self.__ventana = Tk()
        self.__ventana.iconbitmap("icono_juego_simon.ico")
        self.__ventana.title("SIMON Virtual 3D")
        self.__ventana.geometry("512x770")
        self.__ventana.resizable(0, 0)
        self.__ventana.config(background = "#000000")
        self.jsonF = ObjectEncoder()
        self.gestor_jugadores = gestor_jugadores
        barra_menu = Menu(self.__ventana)
        menu_opciones = Menu(barra_menu, tearoff = 0)
        menu_opciones.add_command(label = "Puntaje", command = self.mostrarPuntaje)
        menu_opciones.add_command(label = "Salir", command = self.salirPrograma)
        self.lista_opciones = ["Principiante", "Experto", "Super Experto"]
        niveles_dificultad = ttk.Label(self.__ventana, text = "Seleccione Nivel", background = "black", foreground = "white").grid(row = 1, column = 0)
        self.opcion = ttk.Combobox(self.__ventana, name = niveles_dificultad, width = 13, values = self.lista_opciones, state = "readonly")
        self.opcion.grid(row = 1, column = 1)
        self.opcion.current(0)
        barra_menu.add_cascade(label = "Opciones", menu = menu_opciones)
        self.__ventana.config(menu = barra_menu)
        self.colores_iluminados = {0: "#87FB81", 1: "#F47878", 2: "#F2F587", 3: "#99B7F9"}
        self.colores_originales = {0: "#245400", 1: "#540000", 2: "#6C6400", 3: "#00396C"}
        self.__lista_colores = ["green", "red", "yellow", "blue"]
        self.jugador = self.gestor_jugadores.getJugadorActual()
        self.nombre_jugador = self.jugador.getNombreJugador()
        self.diccionario_partidas = self.gestor_jugadores.toJSON() 
        if len(self.nombre_jugador) == 0:
            self.jugador.setNombreJugador("Sin_Nombre")
            self.nombre_jugador = self.jugador.getNombreJugador()
        self.puntuacion = self.jugador.getPuntajeJugador()
        Label(self.__ventana, text = self.nombre_jugador, bg = "#000000", fg = "#F2F2F2").grid(column = 0, row = 0, padx = 30, sticky = "w")
        self.marcador_puntos = Label(self.__ventana, text = self.puntuacion, bg = "#000000", fg = "#F2F2F2")
        self.marcador_puntos.grid(column = 1, row = 0, sticky = "n")
        self.__boton_verde = Canvas(self.__ventana, background = self.colores_originales[0], highlightbackground = "#000000", relief = "raised", borderwidth = 5, cursor = "hand2")
        self.__boton_verde.config(width = 240, height = 325)
        self.__boton_verde.grid(column = 0, row = 2)
        self.__boton_rojo = Canvas(self.__ventana, background = self.colores_originales[1], highlightbackground = "#000000", relief = "raised", borderwidth = 5, cursor = "hand2")
        self.__boton_rojo.config(width = 240, height = 325)
        self.__boton_rojo.grid(column = 1, row = 2)
        self.__boton_amarillo = Canvas(self.__ventana, background = self.colores_originales[2], highlightbackground = "#000000", relief = "raised", borderwidth = 5, cursor = "hand2")
        self.__boton_amarillo.config(width = 240, height = 325)
        self.__boton_amarillo.grid(column = 0, row = 3)
        self.__boton_azul = Canvas(self.__ventana, background = self.colores_originales[3], highlightbackground = "#000000", relief = "raised", borderwidth = 5, cursor = "hand2")
        self.__boton_azul.config(width = 240, height = 325)
        self.__boton_azul.grid(column = 1, row = 3)
        Button(self.__ventana, text = "Entrar", command = self.empezarNivel, width = 10).grid(row = 4, columnspan=3)
        self.__ventana.mainloop()

if __name__ == '__main__':
    SimonVirtual3D()