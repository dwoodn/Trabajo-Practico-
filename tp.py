# sistema_transporte.py

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import math
from collections import defaultdict
import csv

# --- MODELOS DE DATOS ---

#--- FUNCIONES DE VALIDACION DE VARIABLES

def validar_string(valor, nombre="variable"):
    if not isinstance(valor, str):
        return f"{nombre} debe ser un string."
    if valor.strip() == "":
        return f"{nombre} no puede estar vacío."
    return None

def validar_entero(valor, nombre="variable", min_val=None, max_val=None):
    if not isinstance(valor, int):
        return f"{nombre} debe ser un entero."
    if min_val is not None and valor < min_val:
        return f"{nombre} debe ser mayor o igual a {min_val}."
    if max_val is not None and valor > max_val:
        return f"{nombre} debe ser menor o igual a {max_val}."
    return None

def validar_float(valor, nombre="variable", positivo=False):
    if not isinstance(valor, (int, float)):
        return f"{nombre} debe ser un número (int o float)."
    if positivo and valor <= 0:
        return f"{nombre} debe ser mayor a 0."
    return None

def validar_booleano(valor, nombre="variable"):
    if not isinstance(valor, bool):
        return f"{nombre} debe ser booleano (True o False)."
    return None

def check_datos(nombre, edad, altura, activo):
    errores = []

    if (e := validar_string(nombre, "nombre")): errores.append(e)
    if (e := validar_entero(edad, "edad", 0, 120)): errores.append(e)
    if (e := validar_float(altura, "altura", positivo=True)): errores.append(e)
    if (e := validar_booleano(activo, "activo")): errores.append(e)


@dataclass
class Nodo:
    nombre: str
    modos_transporte: List[str]

@dataclass
class Conexion:
    origen: str
    destino: str
    modo: str
    distancia_km: float
    velocidad_max_kmh: Optional[float] = None
    peso_max_kg: Optional[float] = None

@dataclass
class Vehiculo:
    nombre: str
    modo: str
    velocidad_kmh: float
    capacidad_kg: float
    costo_fijo: float
    costo_km: float
    costo_kg: float

    def calcular_costo(self, distancia_km: float, carga_kg: float) -> float:
        vehiculos_necesarios = math.ceil(carga_kg / self.capacidad_kg)
        return vehiculos_necesarios * (self.costo_fijo + self.costo_km * distancia_km + self.costo_kg * carga_kg)

    def calcular_tiempo(self, distancia_km: float, limite_velocidad: Optional[float] = None) -> float:
        velocidad_efectiva = min(self.velocidad_kmh, limite_velocidad) if limite_velocidad else self.velocidad_kmh
        return distancia_km / velocidad_efectiva

@dataclass
class SolicitudTransporte:
    id_carga: str
    peso_kg: float
    origen: str
    destino: str

@dataclass
class Tramo:
    origen: str
    destino: str
    modo: str
    vehiculo: str
    distancia_km: float
    tiempo_horas: float
    costo: float

@dataclass
class Itinerario:
    tramos: List[Tramo]
    kpi: str

    def tiempo_total(self) -> float:
        return sum(t.tiempo_horas for t in self.tramos)

    def costo_total(self) -> float:
        return sum(t.costo for t in self.tramos)

@dataclass
class RedTransporte:
    nodos: Dict[str, Nodo] = field(default_factory=dict)
    conexiones: List[Conexion] = field(default_factory=list)
    vehiculos: Dict[str, Vehiculo] = field(default_factory=dict)

    def agregar_nodo(self, nodo: Nodo):
        self.nodos[nodo.nombre] = nodo

    def agregar_conexion(self, conexion: Conexion):
        self.conexiones.append(conexion)

    def agregar_vehiculo(self, vehiculo: Vehiculo):
        self.vehiculos[vehiculo.nombre] = vehiculo

# --- PLANIFICADOR ---

@dataclass
class CaminoPosible:
    nodos: List[str]
    conexiones: List[Conexion]

class Planificador:
    def __init__(self, red: RedTransporte):
        self.red = red
        self.grafo = self._construir_grafo()

    def _construir_grafo(self) -> Dict[str, List[Conexion]]:
        grafo = defaultdict(list)
        for conexion in self.red.conexiones:
            grafo[conexion.origen].append(conexion)
        return grafo

    def _camino_sin_loops(self, origen: str, destino: str) -> List[CaminoPosible]:
        caminos = []

        def dfs(actual, visitados, ruta):
            if actual == destino:
                caminos.append(CaminoPosible(nodos=[n for n in visitados], conexiones=list(ruta)))
                return
            for conexion in self.grafo[actual]:
                if conexion.destino not in visitados:
                    visitados.append(conexion.destino)
                    ruta.append(conexion)
                    dfs(conexion.destino, visitados, ruta)
                    ruta.pop()
                    visitados.pop()

        dfs(origen, [origen], [])
        return caminos

    def generar_itinerario(self, solicitud: SolicitudTransporte, kpi: str) -> Optional[Itinerario]:
        caminos = self._camino_sin_loops(solicitud.origen, solicitud.destino)
        mejor_itinerario = None
        mejor_valor = float('inf')

        for camino in caminos:
            tramos = []
            for conexion in camino.conexiones:
                vehiculo = self._seleccionar_vehiculo(conexion, solicitud.peso_kg)
                if not vehiculo:
                    break
                if conexion.peso_max_kg and solicitud.peso_kg > conexion.peso_max_kg:
                    break
                tiempo = vehiculo.calcular_tiempo(conexion.distancia_km, conexion.velocidad_max_kmh)
                costo = vehiculo.calcular_costo(conexion.distancia_km, solicitud.peso_kg)
                tramos.append(Tramo(conexion.origen, conexion.destino, conexion.modo,
                                    vehiculo.nombre, conexion.distancia_km, tiempo, costo))
            else:
                itinerario = Itinerario(tramos, kpi)
                valor = itinerario.tiempo_total() if kpi == "tiempo" else itinerario.costo_total()
                if valor < mejor_valor:
                    mejor_valor = valor
                    mejor_itinerario = itinerario

        return mejor_itinerario

    def _seleccionar_vehiculo(self, conexion: Conexion, peso_kg: float) -> Optional[Vehiculo]:
        candidatos = [v for v in self.red.vehiculos.values() if v.modo == conexion.modo and v.capacidad_kg > 0]
        candidatos_validos = [v for v in candidatos if math.ceil(peso_kg / v.capacidad_kg) >= 1]
        return candidatos_validos[0] if candidatos_validos else None

# --- MAIN (pruebas con CSV o hardcoded) ---

if __name__ == "__main__":
    # Acá podrías cargar los CSV y hacer pruebas llamando a Planificador
    print("Sistema de transporte listo para procesar solicitudes.")
    

