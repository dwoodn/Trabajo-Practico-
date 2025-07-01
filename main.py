import matplotlib.pyplot as plt
from nodo import Nodo 
from conexion import Conexion
from lectura_archivo import LecturaArchivos
from solicitud import leer_solicitudes_csv
from redtransporte import RedTransporte
from vehiculos_especializados import (
    VehiculoFerroviario,
    VehiculoAutomotor,
    VehiculoFluvial,
    VehiculoAereo
)
from planificador_costo import PlanificadorPorCosto
from planificador_tiempo import PlanificadorPorTiempo
# Importar funciones de graficado
from graficos_itinerarios import calcular_acumulados, graficar_distancia_vs_tiempo, graficar_costo_vs_distancia
from graficar_rutas import graficar_grafo_matplotlib


def main():
    # Leer nodos y conexiones desde archivos CSV
    lector = LecturaArchivos()
    lector.leer_nodos("archivos_ejemplo/nodos.csv")
    lector.leer_conexiones("archivos_ejemplo/conexiones.csv")
    nodos, conexiones = lector.obtener_red()

    print("NODOS CARGADOS:")
    for nombre, nodo in nodos.items():
        print(nodo)

    print("\nCONEXIONES CARGADAS:")
    for conexion in conexiones:
        print(conexion)

    # Graficar la red de transporte completa solo con matplotlib
    print("\nGenerando gráfico de la red de transporte...")
    coordenadas = {
        'Zarate': (1, 5),
        'Buenos_Aires': (5, 8),
        'Junin': (3, 2),
        'Azul': (7, 2),
        'Mar_del_Plata': (10, 1),
    }
    graficar_grafo_matplotlib(nodos, conexiones, coordenadas)

    # Crear red de transporte
    red = RedTransporte(nodos, conexiones)

    # Crear vehículos disponibles
    vehiculos = [
        VehiculoFerroviario("Tren de carga"),
        VehiculoAutomotor("Camión estándar"),
        VehiculoFluvial("Barco fluvial", tipo="fluvial"),
        VehiculoFluvial("Barco maritimo", tipo="maritimo"),
        VehiculoAereo("Avión de carga"),
    ]

    # Instanciar planificador
    planificador_costo = PlanificadorPorCosto(red, vehiculos)
    planificador_tiempo = PlanificadorPorTiempo(red, vehiculos)

    # Leer solicitudes desde CSV
    solicitudes = leer_solicitudes_csv("archivos_ejemplo/solicitudes.csv")

    # Procesar cada solicitud
    # por  costo

    for s in solicitudes:
        print(f"\nProcesando solicitud: {s}")
        resultado = planificador_costo.planificar(s.origen, s.destino, s.peso_kg)

        if resultado:
            camino, costo_total, tiempo_total = resultado
            nombres = " -> ".join([c.origen.nombre for c in camino] + [camino[-1].destino.nombre])
            print(f"Camino encontrado: modo {camino[0].modo} -> {nombres}")
            print(f"Costo total: ${costo_total:.2f}")
            # print(f"Tiempo total: {mostrar_horas_minutos(tiempo_total)}")
        else:
            print("No se encontró un camino válido para esta solicitud.")

# por tiempo
 
    for s in solicitudes:
        print(f"\nProcesando solicitud: {s}")
        resultado = planificador_tiempo.planificar(s.origen, s.destino, s.peso_kg)

        if resultado:
            camino, costo_total, tiempo_total = resultado
            nombres = " -> ".join([c.origen.nombre for c in camino] + [camino[-1].destino.nombre])
            print(f"Camino encontrado: modo {camino[0].modo} -> {nombres}")
            # print(f"Costo total: ${costo_total:.2f}")
            print(f"Tiempo total: {mostrar_horas_minutos(tiempo_total)}")
        else:
            print("No se encontró un camino válido para esta solicitud.")

# --- GRAFICAR SOLO LOS 5 MEJORES CAMINOS (MENOR COSTO) PARA CADA SOLICITUD ---
    for s in solicitudes:
        print(f"\nGenerando gráficos para solicitud: {s.origen} -> {s.destino} (peso: {s.peso_kg} kg)")
        caminos = red.buscar_caminos(s.origen, s.destino)
        if not caminos:
            print("No hay caminos posibles para esta solicitud.")
            continue
        # Calcular costo total de cada camino
        caminos_con_costos = []
        for camino in caminos:
            try:
                dist_acum, tiempo_acum, costo_acum, _ = calcular_acumulados(camino, vehiculos, s.peso_kg)
                costo_total = costo_acum[-1]
                caminos_con_costos.append((camino, dist_acum, tiempo_acum, costo_acum, costo_total))
            except Exception as e:
                print(f"Camino descartado por error: {e}")
                continue
        # Ordenar por menor costo total y tomar los 5 mejores
        caminos_con_costos.sort(key=lambda x: x[4])
        mejores = caminos_con_costos[:5]
        if not mejores:
            print("No hay caminos válidos para graficar.")
            continue
        # Gráfico 1: Distancia acumulada vs Tiempo acumulado
        plt.figure(figsize=(10, 5))
        for idx, (camino, dist_acum, tiempo_acum, costo_acum, costo_total) in enumerate(mejores):
            graficar_distancia_vs_tiempo(dist_acum, tiempo_acum, idx)
        plt.title(f"Distancia acumulada vs Tiempo acumulado\n{s.origen} -> {s.destino}")
        plt.tight_layout()
        plt.show()
        # Gráfico 2: Costo acumulado vs Distancia acumulada
        plt.figure(figsize=(10, 5))
        for idx, (camino, dist_acum, tiempo_acum, costo_acum, costo_total) in enumerate(mejores):
            graficar_costo_vs_distancia(dist_acum, costo_acum, idx)
        plt.title(f"Costo acumulado vs Distancia acumulada\n{s.origen} -> {s.destino}")
        plt.tight_layout()
        plt.show()


def mostrar_horas_minutos(tiempo_horas):
    horas = int(tiempo_horas)
    minutos = int((tiempo_horas - horas) * 60)
    return f"{horas}h {minutos}m"


if __name__ == "__main__":
    main()