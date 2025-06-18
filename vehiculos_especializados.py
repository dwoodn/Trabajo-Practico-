from vehiculo import Vehiculo

class VehiculoFerroviario(Vehiculo):
    def __init__(self, nombre):
        super().__init__(nombre, "ferroviaria", 100, 150000, 100, 15, 3)

    def calcular_costo_por_distancia(self, distancia_km, tipo=None):
        costo_km = 20 if distancia_km < 200 else self.costo_km
        return self.costo_base + (costo_km * distancia_km)

class VehiculoAutomotor(Vehiculo):
    def __init__(self, nombre):
        super().__init__(nombre, "automotor", 80, 30000, 30, 5, 0)  # El costo por kg se calcula aparte

    def calcular_costo_por_peso(self, peso_kg):
        costo_kg = 1 if peso_kg < 15000 else 2
        return costo_kg * peso_kg

    def calcular_costo_por_distancia(self, distancia_km, tipo=None):
        return self.costo_base + (self.costo_km * distancia_km)


class VehiculoFluvial(Vehiculo):
    def __init__(self, nombre, tipo="fluvial"):
        super().__init__(nombre, tipo, 40, 100000, 500, 15, 2)


    def calcular_costo_por_distancia(self, distancia_km, tipo=None):
        if tipo == "fluvial":
            costo_base = 500
        elif tipo == "maritimo":
            costo_base = 1500
        else:
            raise ValueError("Tipo de vehículo fluvial no reconocido. Use 'fluvial' o 'maritimo'.")

        return costo_base + (self.costo_km * distancia_km)



class VehiculoAereo(Vehiculo):
    def __init__(self, nombre):
        super().__init__(nombre, "aerea", 600, 5000, 750, 40, 10)
