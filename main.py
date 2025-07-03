import matplotlib.pyplot as plt
from nodo import Nodo 
from conexion import Conexion
from lectura_archivo import LecturaArchivos
from solicitud import leer_solicitudes_csv
from redtransporte import RedTransporte
from vehiculos_modelos import Trochita, Camioneta, Lancha, Avioneta
from planificador_costo import PlanificadorPorCosto
from planificador_tiempo import PlanificadorPorTiempo
# Importar funciones de graficado
from graficos_itinerarios import calcular_acumulados, graficar_distancia_vs_tiempo, graficar_costo_vs_distancia
from graficar_rutas import graficar_grafo_matplotlib
from vehiculos_especializados import VehiculoFerroviario, VehiculoAutomotor, VehiculoFluvial, VehiculoAereo


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
        Trochita(),
        VehiculoAutomotor("Camión estándar"),
        Camioneta(),
        VehiculoFluvial("Barco fluvial", tipo="fluvial"),
        Lancha(),
        VehiculoFluvial("Barco maritimo", tipo="maritimo"),
        VehiculoAereo("Avión de carga"),
        Avioneta(),
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

    # --- PROCESAR SOLICITUDES MANUALES ADICIONALES ---
    solicitudes_adicionales = [
        {"id": "CARGA_001", "origen": "Zarate", "destino": "Mar_del_Plata", "peso_kg": 70000},
        {"id": "CARGA_002", "origen": "Mar_del_Plata", "destino": "Junin", "peso_kg": 100000},
    ]

    for s in solicitudes_adicionales:
        print(f"\nProcesando solicitud manual: {s['id']} ({s['origen']} -> {s['destino']}, {s['peso_kg']} kg)")

        # Por costo
        resultado_costo = planificador_costo.planificar(s['origen'], s['destino'], s['peso_kg'])
        if resultado_costo:
            camino, costo_total, tiempo_total = resultado_costo
            nombres = " -> ".join([c.origen.nombre for c in camino] + [camino[-1].destino.nombre])
            print(f"[Costo] Camino encontrado: modo {camino[0].modo} -> {nombres}")
            print(f"[Costo] Costo total: ${costo_total:.2f}")
        else:
            print("[Costo] No se encontró un camino válido para esta solicitud.")

        # Por tiempo
        resultado_tiempo = planificador_tiempo.planificar(s['origen'], s['destino'], s['peso_kg'])
        if resultado_tiempo:
            camino, costo_total, tiempo_total = resultado_tiempo
            nombres = " -> ".join([c.origen.nombre for c in camino] + [camino[-1].destino.nombre])
            print(f"[Tiempo] Camino encontrado: modo {camino[0].modo} -> {nombres}")
            print(f"[Tiempo] Tiempo total: {mostrar_horas_minutos(tiempo_total)}")
        else:
            print("[Tiempo] No se encontró un camino válido para esta solicitud.")

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
                dist_acum, tiempo_acum, costo_acum, modos = calcular_acumulados(camino, vehiculos, s.peso_kg)
                costo_total = costo_acum[-1]
                caminos_con_costos.append((camino, dist_acum, tiempo_acum, costo_acum, costo_total, modos))
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
        plt.figure(figsize=(12, 6))
        for idx, (camino, dist_acum, tiempo_acum, costo_acum, costo_total, modos) in enumerate(mejores):
            graficar_distancia_vs_tiempo(dist_acum, tiempo_acum, idx, modos)
        plt.title(f"Distancia acumulada vs Tiempo acumulado\n{s.origen} -> {s.destino}")
        plt.tight_layout()
        plt.show()
        # Gráfico 2: Costo acumulado vs Distancia acumulada
        plt.figure(figsize=(12, 6))
        for idx, (camino, dist_acum, tiempo_acum, costo_acum, costo_total, modos) in enumerate(mejores):
            graficar_costo_vs_distancia(dist_acum, costo_acum, idx, modos)
        plt.title(f"Costo acumulado vs Distancia acumulada\n{s.origen} -> {s.destino}")
        plt.tight_layout()
        plt.show()

    # --- OPTIMIZAR POR VEHÍCULO ESPECÍFICO PARA CARGA_001 Y CARGA_002 ---
    print("\n--- OPTIMIZACIÓN POR VEHÍCULO ESPECÍFICO (CARGA_001 y CARGA_002) ---")
    cargas = [
        {"id": "CARGA_001", "origen": "Zarate", "destino": "Mar_del_Plata", "peso_kg": 70000},
        {"id": "CARGA_002", "origen": "Mar_del_Plata", "destino": "Junin", "peso_kg": 100000},
    ]
    for carga in cargas:
        print(f"\nCarga: {carga['id']} ({carga['origen']} -> {carga['destino']}, {carga['peso_kg']} kg)")
        mejor_costo = None
        mejor_tiempo = None
        vehiculo_costo = None
        vehiculo_tiempo = None
        for v in vehiculos:
            planificador = type(planificador_costo)(red, [v])
            resultado = planificador.planificar(carga['origen'], carga['destino'], carga['peso_kg'])
            if resultado:
                camino, costo_total, tiempo_total = resultado
                if mejor_costo is None or costo_total < mejor_costo:
                    mejor_costo = costo_total
                    vehiculo_costo = v
                if mejor_tiempo is None or tiempo_total < mejor_tiempo:
                    mejor_tiempo = tiempo_total
                    vehiculo_tiempo = v
        if vehiculo_costo:
            print(f"Vehículo óptimo por COSTO: {vehiculo_costo.nombre} (Costo: ${mejor_costo:.2f})")
        else:
            print("No hay vehículo válido para minimizar COSTO.")
        if vehiculo_tiempo:
            print(f"Vehículo óptimo por TIEMPO: {vehiculo_tiempo.nombre} (Tiempo: {mostrar_horas_minutos(mejor_tiempo)})")
        else:
            print("No hay vehículo válido para minimizar TIEMPO.")


def mostrar_horas_minutos(tiempo_horas):
    horas = int(tiempo_horas)
    minutos = int((tiempo_horas - horas) * 60)
    return f"{horas}h {minutos}m"


if __name__ == "__main__":
    main()