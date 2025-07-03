from vehiculos_especializados import VehiculoFerroviario, VehiculoAutomotor, VehiculoFluvial, VehiculoAereo

class Trochita(VehiculoFerroviario):
    def __init__(self, nombre="Trochita", velocidad_kmh=50, capacidad_kg=10000, costo_base=10, costo_por_km=500, costo_por_kg=2):
        super().__init__(
            nombre=nombre,
            velocidad_kmh=velocidad_kmh,
            capacidad_kg=capacidad_kg,
            costo_base=costo_base,
            costo_por_km=costo_por_km,
            costo_por_kg=costo_por_kg
        )

    def calcular_costo_por_distancia(self, distancia_km, tipo=None):
        return self.costo_base + (self.costo_km * distancia_km)

    def calcular_costo_por_peso(self, peso_kg):
        return self.costo_kg * peso_kg

class Camioneta(VehiculoAutomotor):
    def __init__(self, nombre="Camioneta", velocidad_kmh=60, capacidad_kg=4000, costo_base=25, costo_por_km=4, costo_por_kg=0.5):
        super().__init__(
            nombre=nombre,
            velocidad_kmh=velocidad_kmh,
            capacidad_kg=capacidad_kg,
            costo_base=costo_base,
            costo_por_km=costo_por_km,
            costo_por_kg=costo_por_kg
        )

    def calcular_costo_por_peso(self, peso_kg):
        return self.costo_kg * peso_kg

    def calcular_costo_por_distancia(self, distancia_km, tipo=None):
        return self.costo_base + (self.costo_km * distancia_km)

class Lancha(VehiculoFluvial):
    def __init__(self, nombre="Lancha", tipo="fluvial", velocidad_kmh=70, capacidad_kg=2000, costo_por_km=10, costo_por_kg=1.5):
        super().__init__(
            nombre=nombre,
            tipo=tipo,
            velocidad_kmh=velocidad_kmh,
            capacidad_kg=capacidad_kg,
            costo_por_km=costo_por_km,
            costo_por_kg=costo_por_kg
        )

class Avioneta(VehiculoAereo):
    def __init__(self, nombre="Avioneta", velocidad_kmh=200, capacidad_kg=500, costo_base=400, costo_por_km=20, costo_por_kg=5):
        super().__init__(
            nombre=nombre,
            velocidad_kmh=velocidad_kmh,
            capacidad_kg=capacidad_kg,
            costo_base=costo_base,
            costo_por_km=costo_por_km,
            costo_por_kg=costo_por_kg
        ) 