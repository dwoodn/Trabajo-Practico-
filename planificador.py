from vehiculo import Vehiculo


class Planificador:
    def __init__(self, red, vehiculos):
        self.red = red
        self.vehiculos = vehiculos  # lista de instancias de Vehiculo

    def seleccionar_vehiculo(self, modo, peso_kg):
        candidatos = [v for v in self.vehiculos if v.modo == modo]
        return candidatos[0] if candidatos else None

    def evaluar_camino(self, camino, peso_kg):
        total_costo = 0
        total_tiempo = 0
        primer_tramo = camino[0]

        vehiculo: Vehiculo = self.seleccionar_vehiculo(primer_tramo.modo, peso_kg)
        if vehiculo is None:
            raise Exception("No se encontró un vehículo para el modo de transporte.")

        cantidad_viajes = int(-(-peso_kg // vehiculo.capacidad))  # redondeo hacia arriba
        costo_por_peso = 0.0

        for i in range(cantidad_viajes):
            peso_envio = vehiculo.capacidad if i < cantidad_viajes - 1 else peso_kg % vehiculo.capacidad
            if peso_envio == 0:
                peso_envio = vehiculo.capacidad
            costo_por_peso += vehiculo.calcular_costo_por_peso(peso_envio)

        for tramo in camino:
            if not tramo.es_valida_para(vehiculo, peso_kg):
                raise Exception("Vehículo no válido para este tramo.")

            tipo_camino = tramo.restricciones.get("tipo", None)
            costo_total_tramo = vehiculo.calcular_costo_por_distancia(tramo.distancia, tipo_camino)

            velocidad_maxima = tramo.restricciones.get("velocidad_max", vehiculo.velocidad)
            velocidad = min(vehiculo.velocidad, velocidad_maxima)
            tiempo_tramo = tramo.distancia / velocidad

            total_costo += costo_total_tramo * cantidad_viajes
            total_tiempo += tiempo_tramo

        total_costo += costo_por_peso
        return total_costo, total_tiempo

    def planificar(self, origen, destino, peso_kg, kpi="costo"):
        modos_disponibles = ["automotor", "ferroviaria", "aerea", "fluvial"]
        mejores = []

        for modo in modos_disponibles:
            caminos = self.red.buscar_caminos(origen, destino, modo)

            for camino in caminos:
                try:
                    costo, tiempo = self.evaluar_camino(camino, peso_kg)
                    mejores.append((camino, costo, tiempo))
                except:
                    continue  # descartar caminos inválidos

        if not mejores:
            return None

        if kpi == "costo":
            return min(mejores, key=lambda x: x[1])
        elif kpi == "tiempo":
            return min(mejores, key=lambda x: x[2])
        else:
            raise ValueError("KPI no válido. Debe ser 'costo' o 'tiempo'.")
