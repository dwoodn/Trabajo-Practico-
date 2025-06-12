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
from planificador import Planificador

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

    # Crear red de transporte
    red = RedTransporte(nodos, conexiones)

    # Crear vehículos disponibles
    vehiculos = [
        VehiculoFerroviario("Tren de carga"),
        VehiculoAutomotor("Camión estándar"),
        VehiculoFluvial("Barco fluvial", tipo="fluvial"),
        VehiculoFluvial("Barco marítimo", tipo="marítimo"),
        VehiculoAereo("Avión de carga"),
    ]

    # Instanciar planificador
    planificador = Planificador(red, vehiculos)

    # Leer solicitudes desde CSV
    solicitudes = leer_solicitudes_csv("archivos_ejemplo/solicitudes.csv")

    # Procesar cada solicitud
    for s in solicitudes:
        print(f"\nProcesando solicitud: {s}")
        resultado = planificador.planificar(origen=s.origen, destino=s.destino, peso_kg=s.peso_kg, kpi="costo")

        if resultado:
            camino, costo_total, tiempo_total = resultado
            nombres = " -> ".join([c.origen.nombre for c in camino] + [camino[-1].destino.nombre])
            print(f"Camino encontrado: modo {camino[0].modo} -> {nombres}")
            print(f"Costo total: ${costo_total:.2f}")
            # print(f"Tiempo total: {mostrar_horas_minutos(tiempo_total)}")
        else:
            print("No se encontró un camino válido para esta solicitud.")


    for s in solicitudes:
        print(f"\nProcesando solicitud: {s}")
        resultado = planificador.planificar(origen=s.origen, destino=s.destino, peso_kg=s.peso_kg, kpi="tiempo")

        if resultado:
            camino, costo_total, tiempo_total = resultado
            nombres = " -> ".join([c.origen.nombre for c in camino] + [camino[-1].destino.nombre])
            print(f"Camino encontrado: modo {camino[0].modo} -> {nombres}")
            # print(f"Costo total: ${costo_total:.2f}")
            print(f"Tiempo total: {mostrar_horas_minutos(tiempo_total)}")
        else:
            print("No se encontró un camino válido para esta solicitud.")


def mostrar_horas_minutos(tiempo_horas):
    horas = int(tiempo_horas)
    minutos = int((tiempo_horas - horas) * 60)
    return f"{horas}h {minutos}m"


if _name_ == "_main_":
    main()