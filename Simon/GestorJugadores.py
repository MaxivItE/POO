from ClaseJugador import Jugador
from datetime import datetime

class GestorJugadores:
    __lista_jugadores: list
    __jugador_actual: object
    __fecha: str
    __hora: str

    def __init__(self):
        self.__lista_jugadores = []
    
    def addJugador(self, nombre_jugador, tiempo_jugador):
        self.getFechaActual()
        unJugador = Jugador(nombre_jugador, tiempo_jugador, self.__fecha, self.__hora)
        self.__jugador_actual = unJugador

    def getJugadorActual(self):
        return self.__jugador_actual
    
    def getFechaActual(self):
        fecha_actual = datetime.now()
        self.__fecha = fecha_actual.strftime('%d/%m/%Y')
        self.__hora = fecha_actual.strftime("%H:%M")

    def guardarPartida(self, unJugador):
        self.getFechaActual()
        self.__lista_jugadores.append(unJugador)
    
    def getListaJugadores(self):
        return self.__lista_jugadores

    def ordenar_por_puntaje(self):
        min_index: int = 0
        min_value: int = 0
        aux: list = []
        tamano_lista_punuacion: int = len(self.__lista_jugadores)-1
        for i in range(0, tamano_lista_punuacion):
            min_index = i
            min_value = self.__lista_jugadores[min_index]
            for j in range(i, tamano_lista_punuacion):
                if min_value < self.__lista_jugadores[j+1]:
                    min_value = self.__lista_jugadores[j+1]
                    min_index = j+1
            if min_index != 1:
                aux = self.__lista_jugadores[i]
                self.__lista_jugadores[i] = self.__lista_jugadores[min_index]
                self.__lista_jugadores[min_index] = aux
    
    def toJSON(self):  #Despues de almacenar las partidas en el diccioanrio, se va a la función guardarJSONArhcivo para guardar las partidas en el archivo JSON
        diccionario_partidas = dict(
            __class__ = self.__class__.__name__,
            partidas = [partida.toJSON() for partida in self.__lista_jugadores]
        )
        return diccionario_partidas

    def mostrarDatos(self):
        print("DATOS PARTIDAS")
        for i in range(len(self.__lista_jugadores)):
            print(self.__lista_jugadores[i])