import csv
from nodo import Nodo
from conexion import Conexion

class LecturaArchivos:
    def __init__(self):
        self.nodos = {}
        self.conexiones = []

    def leer_nodos(self, ruta_archivo):
        with open(ruta_archivo, newline='') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                nombre = fila["nombre"]
                nodo = Nodo(nombre)
                self.nodos[nombre] = nodo
    def leer_conexiones(self, ruta_archivo):
        with open(ruta_archivo, newline='') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                origen_nombre = fila["origen"]
                destino_nombre = fila["destino"]
                modo = fila["tipo"].lower()
                distancia = float(fila["distancia_km"])
            
                restricciones = {}
                if fila["restriccion"]:  # si no está vacío
                    restricciones[fila["restriccion"]] = (
                        float(fila["valor_restriccion"])
                        if fila["valor_restriccion"].replace(".", "", 1).isdigit()
                        else fila["valor_restriccion"]
                )

                origen = self.nodos.get(origen_nombre)
                destino = self.nodos.get(destino_nombre)
            
                if origen and destino:
                    # Conexión original
                    conexion = Conexion(origen, destino, modo, distancia, restricciones)
                    self.conexiones.append(conexion)
                    origen.agregar_conexion(conexion)
                    # Conexión inversa (bidireccional)
                    conexion_inversa = Conexion(destino, origen, modo, distancia, restricciones)
                    self.conexiones.append(conexion_inversa)
                    destino.agregar_conexion(conexion_inversa)


    def obtener_red(self):
        return self.nodos, self.conexiones
