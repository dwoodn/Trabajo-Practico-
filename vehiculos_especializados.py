from vehiculo import Vehiculo

class VehiculoFerroviario(Vehiculo):
    def __init__(self, nombre):
        super().__init__(
            nombre=nombre,
            modo="ferroviaria",
            velocidad_kmh=100,
            capacidad_kg=150000,
            costo_base=100,
            costo_por_km=15,
            costo_por_kg=3
        )

    def calcular_costo_por_peso(self, peso_kg):
        return self.costo_kg * peso_kg

    def calcular_costo_por_distancia(self, distancia_km, tipo=None):
        costo_km = 20 if distancia_km < 200 else self.costo_km
        return self.costo_base + (costo_km * distancia_km)

class VehiculoAutomotor(Vehiculo):
    def __init__(self, nombre):
        super().__init__(
            nombre=nombre,
            modo="automotor",
            velocidad_kmh=80,
            capacidad_kg=30000,
            costo_base=30,
            costo_por_km=5,
            costo_por_kg=0  
        )

    def calcular_costo_por_peso(self, peso_kg):
        costo_unitario = 1 if peso_kg < 15000 else 2
        return costo_unitario * peso_kg

class VehiculoFluvial(Vehiculo):
    def __init__(self, nombre, tipo="fluvial"):
        if tipo == "fluvial":
            costo_base = 500
        elif tipo == "maritimo":
            costo_base = 1500
        else:
            raise ValueError("Tipo inválido. Use 'fluvial' o 'maritimo'.")

        super().__init__(
            nombre=nombre,
            modo=tipo,  
            velocidad_kmh=40,
            capacidad_kg=100000,
            costo_base=costo_base,
            costo_por_km=15,
            costo_por_kg=2
        )

    def calcular_costo_por_peso(self, peso_kg):
        return self.costo_kg * peso_kg

    def calcular_costo_por_distancia(self, distancia_km, tipo=None):
        return self.costo_base + (self.costo_km * distancia_km)

class VehiculoAereo(Vehiculo):
    def __init__(self, nombre):
        super().__init__(
            nombre=nombre,
            modo="aerea",
            velocidad_kmh=600,
            capacidad_kg=5000,
            costo_base=750,
            costo_por_km=40,
            costo_por_kg=10
        )

    def calcular_costo_por_peso(self, peso_kg):
        return self.costo_kg * peso_kg

    def calcular_costo_por_distancia(self, distancia_km, tipo=None):
        return self.costo_base + (self.costo_km * distancia_km)


