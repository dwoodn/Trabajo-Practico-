import matplotlib.pyplot as plt
import numpy as np
from lectura_archivo import LecturaArchivos
from redtransporte import RedTransporte
from vehiculos_especializados import VehiculoFerroviario, VehiculoAutomotor, VehiculoFluvial, VehiculoAereo

# Asume que cada tramo es una instancia de Conexion y que tienes una lista de vehiculos disponibles

def ajustar_posicion_etiqueta(x, y, posiciones_usadas, min_dist=0.1):
    """Ajusta la posición de una etiqueta para evitar superposición"""
    offsets = [(10, 10), (-10, 10), (10, -10), (-10, -10),
               (0, 20), (20, 0), (-20, 0), (0, -20)]
    
    for dx, dy in offsets:
        nueva_pos = (x + dx/100, y + dy/100)
        # Verificar si esta posición está lo suficientemente lejos de las otras
        if all(np.sqrt((px-nueva_pos[0])**2 + (py-nueva_pos[1])**2) > min_dist 
               for px, py in posiciones_usadas):
            posiciones_usadas.append(nueva_pos)
            return dx, dy
    return 10, 10  # posición por defecto si no se encuentra una mejor

def graficar_distancia_vs_tiempo(dist_acum, tiempo_acum, idx, vehiculos_usados=None):
    """
    Grafica la distancia acumulada vs tiempo acumulado para un camino.
    Los puntos representan las ciudades intermedias del recorrido.
    """
    estilos_linea = ['-', '--', ':', '-.', '-']
    if vehiculos_usados:
        if len(vehiculos_usados) > 1:
            secuencia = []
            actual = vehiculos_usados[0]
            contador = 1
            for i in range(1, len(vehiculos_usados)):
                if vehiculos_usados[i] == actual:
                    contador += 1
                else:
                    if contador > 1:
                        secuencia.append(f"{actual}({contador})")
                    else:
                        secuencia.append(actual)
                    actual = vehiculos_usados[i]
                    contador = 1
            if contador > 1:
                secuencia.append(f"{actual}({contador})")
            else:
                secuencia.append(actual)
            etiqueta = f'Camino {idx+1} ({" → ".join(secuencia)})'
        else:
            etiqueta = f'Camino {idx+1} ({vehiculos_usados[0]})'
    else:
        etiqueta = f'Camino {idx+1}'
    plt.plot(tiempo_acum, dist_acum, 
             linestyle=estilos_linea[idx % len(estilos_linea)],
             marker='o', label=etiqueta, linewidth=2)
    plt.xlabel('Tiempo acumulado (horas)')
    plt.ylabel('Distancia acumulada (km)')
    plt.title('Progreso de la carga en el tiempo\nCada punto representa una ciudad del recorrido')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

def graficar_costo_vs_distancia(dist_acum, costo_acum, idx, vehiculos_usados=None):
    """
    Grafica el costo acumulado vs distancia acumulada para un camino.
    Los puntos representan las ciudades intermedias del recorrido.
    """
    estilos_linea = ['-', '--', ':', '-.', '-']
    if vehiculos_usados:
        if len(vehiculos_usados) > 1:
            secuencia = []
            actual = vehiculos_usados[0]
            contador = 1
            for i in range(1, len(vehiculos_usados)):
                if vehiculos_usados[i] == actual:
                    contador += 1
                else:
                    if contador > 1:
                        secuencia.append(f"{actual}({contador})")
                    else:
                        secuencia.append(actual)
                    actual = vehiculos_usados[i]
                    contador = 1
            if contador > 1:
                secuencia.append(f"{actual}({contador})")
            else:
                secuencia.append(actual)
            etiqueta = f'Camino {idx+1} ({" → ".join(secuencia)})'
        else:
            etiqueta = f'Camino {idx+1} ({vehiculos_usados[0]})'
    else:
        etiqueta = f'Camino {idx+1}'
    plt.plot(dist_acum, costo_acum, 
             linestyle=estilos_linea[idx % len(estilos_linea)],
             marker='o', label=etiqueta, linewidth=2)
    plt.xlabel('Distancia acumulada (km)')
    plt.ylabel('Costo acumulado ($)')
    plt.title('Evolución del costo según la distancia recorrida\nCada punto representa una ciudad del recorrido')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

def calcular_acumulados(camino, vehiculos, peso_kg):
    """
    Para un camino (lista de conexiones), calcula:
    - distancias acumuladas
    - tiempos acumulados
    - costos acumulados
    usando la lógica de selección de vehículo y cálculo de tu código.
    Además, devuelve la lista de nombres de vehículos usados en cada tramo.
    Para cada tramo, selecciona el vehículo óptimo (menor costo total para ese tramo).
    """
    dist_acum = [0]
    tiempo_acum = [0]
    costo_acum = [0]
    vehiculos_usados = []  # Lista para guardar el nombre del vehículo de cada tramo
    total_dist = 0
    total_tiempo = 0
    total_costo = 0
    for conexion in camino:
        tipo = conexion.restricciones.get('tipo', None)
        # Buscar el vehículo óptimo (menor costo total para este tramo)
        vehiculo_costo = []
        for v in vehiculos:
            if v.modo == conexion.modo and conexion.es_valida_para(v, peso_kg):
                costo = v.calcular_costo_por_distancia(conexion.distancia, tipo=tipo) + v.calcular_costo_por_peso(peso_kg)
                vehiculo_costo.append((v, costo))
        if not vehiculo_costo:
            raise Exception(f"No hay vehículo válido para modo {conexion.modo}")
        vehiculo, costo = min(vehiculo_costo, key=lambda x: x[1])
        vehiculos_usados.append(vehiculo.nombre)
        velocidad = min(vehiculo.velocidad, conexion.restricciones.get("velocidad_maxima", vehiculo.velocidad))
        tiempo = conexion.distancia / velocidad
        total_dist += conexion.distancia
        total_tiempo += tiempo
        total_costo += costo
        dist_acum.append(total_dist)
        tiempo_acum.append(total_tiempo)
        costo_acum.append(total_costo)
    return dist_acum, tiempo_acum, costo_acum, vehiculos_usados

# Ejemplo de uso
if __name__ == "__main__":
    # Leer red y vehículos
    lector = LecturaArchivos()
    lector.leer_nodos("archivos_ejemplo/nodos.csv")
    lector.leer_conexiones("archivos_ejemplo/conexiones.csv")
    nodos, conexiones = lector.obtener_red()
    red = RedTransporte(nodos, conexiones)
    vehiculos = [
        VehiculoFerroviario("Tren de carga"),
        VehiculoAutomotor("Camión estándar"),
        VehiculoFluvial("Barco fluvial", tipo="fluvial"),
        VehiculoFluvial("Barco maritimo", tipo="maritimo"),
        VehiculoAereo("Avión de carga"),
    ]
    # Parámetros de ejemplo
    origen = 'Zarate'
    destino = 'Mar_del_Plata'
    peso_kg = 10000
    caminos = red.buscar_caminos(origen, destino)
    # Graficar todos los caminos
    plt.figure(figsize=(10, 5))
    for idx, camino in enumerate(caminos):
        dist_acum, tiempo_acum, costo_acum, vehiculos_usados = calcular_acumulados(camino, vehiculos, peso_kg)
        graficar_distancia_vs_tiempo(dist_acum, tiempo_acum, idx, vehiculos_usados)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    for idx, camino in enumerate(caminos):
        dist_acum, tiempo_acum, costo_acum, vehiculos_usados = calcular_acumulados(camino, vehiculos, peso_kg)
        graficar_costo_vs_distancia(dist_acum, costo_acum, idx, vehiculos_usados)
    plt.tight_layout()
    plt.show()