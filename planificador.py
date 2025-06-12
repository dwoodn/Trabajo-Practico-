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
        for tramo in camino:
            vehiculo = self.seleccionar_vehiculo(tramo.modo, peso_kg)
            if vehiculo is None or not tramo.es_valida_para(vehiculo, peso_kg):
                raise Exception("Vehículo no válido para este tramo.")

            # calcular número de viajes necesarios
            cantidad_viajes = -(-peso_kg // vehiculo.capacidad)  # redondeo hacia arriba
            costo_total_tramo = cantidad_viajes * vehiculo.calcular_costo(tramo.distancia, peso_kg)
            tiempo_tramo = tramo.distancia / min(vehiculo.velocidad, tramo.restricciones.get("velocidad_maxima", vehiculo.velocidad))

            total_costo += costo_total_tramo
            total_tiempo += tiempo_tramo

        return total_costo, total_tiempo
    

    def planificar(self, origen, destino, peso_kg, kpi="costo", modo=None):
        caminos = self.red.buscar_caminos(origen, destino, modo)
        mejores = []

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
        else:
            return min(mejores, key=lambda x: x[2])
        # if kpi == "costo":
        #     return min(mejores, key=lambda x: x[1])  # retornar el camino con menor costo
        # else:
        #     return min(mejores, key=lambda x: x[2])  # retornar el camino con menor tiempo
        # return mejores  # retornar todos los caminos con sus costos y tiempos Esto seria una opcion
        
