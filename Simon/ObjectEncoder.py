import json
from pathlib import Path
from GestorJugadores import GestorJugadores
from ClaseJugador import Jugador

class ObjectEncoder():

    def guardarJSONArchivo(self, diccionario_partidas, archivo_puntuaciones):
        with Path(archivo_puntuaciones).open(mode = "w", encoding = "UTF-8") as destino_archivo:
            json.dump(diccionario_partidas, destino_archivo, indent = 4)
    
    def leerJSONArchivo(self, archivo_puntuaciones):  #Lee el archivo y lo almacena en un diccionario para despúes en la función decodificarDiccionario lo desifre
        try:
            with Path(archivo_puntuaciones).open(encoding = "UTF-8") as fuente_archivo:
                diccionario_puntuaciones = json.load(fuente_archivo)
                fuente_archivo.close()
        except:
            return 0
        else:
            return diccionario_puntuaciones

    def decodificadorDiccionario(self, diccionario_puntuaciones):
        if '__class__' not in diccionario_puntuaciones:
            return diccionario_puntuaciones
        else:
            nombre_clase = diccionario_puntuaciones["__class__"]
            #class_ = eval(nombre_clase)
            if nombre_clase == 'GestorJugadores':
                partidas = diccionario_puntuaciones["partidas"]
                gestor_jugadores = GestorJugadores()
                for i in range(len(partidas)):
                    diccionario_puntuaciones = partidas[i]
                    nombre_clase = diccionario_puntuaciones.pop('__class__')
                    #class_ = eval(nombre_clase)
                    datos_partidas = diccionario_puntuaciones['__datos_partidas__']
                    unaPartida = Jugador(**datos_partidas)
                    gestor_jugadores.guardarPartida(unaPartida)
            return gestor_jugadores