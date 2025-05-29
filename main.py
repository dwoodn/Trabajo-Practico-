class Nodo:
    def __init__(self, nombre):
        """
        Crea un nodo identificado por el nombre de la ciudad.

        Args:
            nombre (str): nombre del nodo/ciudad
        """
        self.nombre = nombre
        self.modos = set()        # modos disponibles (automotor, ferroviario, etc.)
        self.conexiones = []      # lista de conexiones salientes

    def agregar_conexion(self, conexion):
        """
        Agrega una conexión saliente desde este nodo.

        Args:
            conexion (Conexion): objeto de tipo Conexion
        """
        self.conexiones.append(conexion)
        self.modos.add(conexion.modo)

    def soporta_modo(self, modo):
        """
        Verifica si el nodo soporta un modo de transporte.

        Args:
            modo (str): nombre del modo

        Returns:
            bool: True si soporta ese modo, False si no.
        """
        return modo in self.modos

    def __str__(self):
        return f"Nodo: {self.nombre} | Modos disponibles: {', '.join(self.modos)}"
    
#ejemplo de uso
nodo1 = Nodo("Bahía Blanca")
nodo2 = Nodo("La Plata")
print(nodo1)

class Conexion:
    def __init__(self, origen, destino, modo, distancia_km, restricciones=None):
        """
        Crea una conexión entre dos nodos con modo de transporte y restricciones específicas.

        Args:
            origen (Nodo): nodo de origen
            destino (Nodo): nodo de destino
            modo (str): modo de transporte
            distancia_km (float): distancia en km
            restricciones (dict): restricciones específicas según el modo
        """
        self.origen = origen
        self.destino = destino
        self.modo = modo.lower()
        self.distancia = distancia_km
        self.restricciones = restricciones or {}

    def es_valida_para(self, vehiculo, peso_envio):
        """
        Verifica si un vehículo puede transitar esta conexión para cierto peso.

        Args:
            vehiculo (Vehiculo): instancia de vehículo
            peso_envio (float): peso del envío en kg

        Returns:
            bool: True si es transitable, False si no.
        """
        if self.modo != vehiculo.modo:
            return False

        if self.modo == "ferroviario":
            vel_max = self.restricciones.get("velocidad_maxima")
            if vel_max and vehiculo.velocidad > vel_max:
                return False

        elif self.modo == "automotor":
            peso_max = self.restricciones.get("peso_maximo")
            if peso_max and peso_envio > peso_max:
                return False

        # Aéreo y marítimo no tienen validación estricta por ahora
        return True

    def __str__(self):
        return (f"{self.modo.upper()} | {self.origen.nombre} ➜ {self.destino.nombre} "
                f"({self.distancia} km) | Restricciones: {self.restricciones}")
    
    # Crear nodos
bahia = Nodo("Bahía Blanca")
laplata = Nodo("La Plata")

# Crear una conexión ferroviaria con límite de velocidad
conexion_ferro = Conexion(
    origen=bahia,
    destino=laplata,
    modo="ferroviario",
    distancia_km=550,
    restricciones={"velocidad_maxima": 90}
)

# Asociar la conexión a los nodos
bahia.agregar_conexion(conexion_ferro)
laplata.agregar_conexion(conexion_ferro)

# Ver
print(bahia)
print(laplata)
print(conexion_ferro)
 
class Vehiculo:
    def __init__(self, nombre, modo, velocidad_kmh, capacidad_kg,
                 costo_base, costo_por_km, costo_por_kg):
        """
        Crea un vehículo con sus características operativas.

        Args:
            nombre (str): nombre del modelo del vehículo
            modo (str): tipo de transporte (automotor, ferroviario, aéreo, marítimo)
            velocidad_kmh (float): velocidad nominal del vehículo
            capacidad_kg (float): carga máxima que puede transportar
            costo_base (float): costo fijo por tramo
            costo_por_km (float): costo variable por kilómetro
            costo_por_kg (float): costo variable por kilo transportado
        """
        self.nombre = nombre
        self.modo = modo.lower()
        self.velocidad = velocidad_kmh
        self.capacidad = capacidad_kg
        self.costo_base = costo_base
        self.costo_km = costo_por_km
        self.costo_kg = costo_por_kg

    def calcular_costo(self, distancia_km, peso_kg):
        """
        Calcula el costo total de un tramo según distancia y peso.

        Returns:
            float: costo total
        """
        return self.costo_base + (self.costo_km * distancia_km) + (self.costo_kg * peso_kg)

    def __str__(self):
        return (f"{self.nombre} [{self.modo.upper()}] | Velocidad: {self.velocidad} km/h | "
                f"Capacidad: {self.capacidad} kg | Costos: Base ${self.costo_base}, "
                f"xKm ${self.costo_km}, xKg ${self.costo_kg}")
    #ejemplo de uso 
    
camion = Vehiculo(
    nombre="Camión Estándar",
    modo="automotor",
    velocidad_kmh=80,
    capacidad_kg=10000,
    costo_base=200,
    costo_por_km=5,
    costo_por_kg=0.1
)

# Calcular costo de un tramo de 100 km y 5000 kg
costo = camion.calcular_costo(distancia_km=100, peso_kg=5000)

print(camion)
print(f"Costo del tramo: ${costo}")   

class Solicitud:
    def __init__(self, id_carga, peso_kg, origen, destino):
        """
        Representa una solicitud de transporte de carga.

        Args:
            id_carga (str): identificador único de la carga
            peso_kg (float): peso total de la carga en kg
            origen (str): nombre del nodo de origen
            destino (str): nombre del nodo de destino
        """
        self.id_carga = id_carga
        self.peso_kg = peso_kg
        self.origen = origen
        self.destino = destino


    def __str__(self):
        return (f"Carga ID: {self.id_carga} | Peso: {self.peso_kg} kg | "
                f"Origen: {self.origen} ➜ Destino: {self.destino}")
solicitud1 = Solicitud(
    id_carga="CARGA123",
    peso_kg=7500,
    origen="Bahía Blanca",
    destino="La Plata"
)

print(solicitud1)

import csv

def leer_solicitudes_csv(ruta_archivo):
    solicitudes = []
    with open(ruta_archivo, newline='', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            solicitud = Solicitud(
                id_carga=fila["id_carga"],
                peso_kg=float(fila["peso_kg"]),
                origen=fila["origen"],
                destino=fila["destino"]
            )
            solicitudes.append(solicitud)
    return solicitudes
