
class Jugador:
    __nombre_jugador: str
    __puntaje: str
    __fecha: str
    __hora: str

    def __init__(self, nombre_jugador, puntaje, fecha, hora):
        self.__nombre_jugador = nombre_jugador
        self.__puntaje = puntaje
        self.__fecha = fecha
        self.__hora = hora
    
    def getNombreJugador(self):
        return self.__nombre_jugador
    
    def setNombreJugador(self, nombre_jugador):
        self.__nombre_jugador = nombre_jugador

    def getPuntajeJugador(self):
        return self.__puntaje

    def setPuntajeJugador(self, puntuacion_total):
        self.__puntaje = puntuacion_total
    
    def getFechaPartida(self):
        return self.__fecha
    
    def getHoraPartida(self):
        return self.__hora

    def toJSON(self):
        diccionario_partida = dict(
            __class__ = self.__class__.__name__,
            __datos_partidas__ = dict(
                nombre_jugador = self.__nombre_jugador,
                fecha = self.__fecha,
                hora = self.__hora,
                puntaje = self.__puntaje
            )
        )
        return diccionario_partida
    
    def __gt__(self,otro_jugador):
        return self.__puntaje > otro_jugador.__puntaje

    def __str__(self):
        return '\n Nombre: {}\n Fecha: {}\n Hora: {}\n Puntaje: {}' .format(self.__nombre_jugador, self.__fecha, self.__hora, self.__puntaje)