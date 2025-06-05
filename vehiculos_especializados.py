from vehiculo import Vehiculo

class VehiculoFerroviario(Vehiculo):
    def __init__(self, nombre):
        super().__init__(nombre, "ferroviario", 100, 150000, 100, 15, 3)


class VehiculoAutomotor(Vehiculo):
    def __init__(self, nombre):
        super().__init__(nombre, "automotor", 80, 30000, 30, 5, 0)  # El costo por kg se calcula aparte

    def calcular_costo(self, distancia_km, peso_kg):
        costo_kg = 1 if peso_kg < 15000 else 2
        return self.costo_base + (5 * distancia_km) + (costo_kg * peso_kg)


class VehiculoMaritimo(Vehiculo):
    def __init__(self, nombre, tipo="marítimo"):
        costo_base = 500 if tipo == "fluvial" else 1500
        super().__init__(nombre, tipo, 40, 100000, costo_base, 15, 2)


class VehiculoAereo(Vehiculo):
    def __init__(self, nombre):
        super().__init__(nombre, "aéreo", 600, 5000, 750, 40, 10)

